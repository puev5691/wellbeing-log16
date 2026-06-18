#!/usr/bin/env python3
from pathlib import Path
import argparse, datetime, json, re, tarfile, tempfile, shutil, sys, hashlib

ROOT = Path('/data/wellbeing/obs/log16')

STATUS_MAP = {
    'FOUND': 'generated',
    'FOUND_EVIDENCE_NEEDS_REVIEW': 'accepted_partial',
    'NEEDS_HUMAN_CONFIRMATION': 'needs_review',
    'NO_EVIDENCE': 'needs_review',
}

PATTERN_DEFAULT = 'research_digest'


def read_text(path):
    return Path(path).read_text(encoding='utf-8', errors='replace')


def find_file(root, rel):
    p = Path(root) / rel
    if p.exists():
        return p
    hits = list(Path(root).rglob(Path(rel).name))
    for h in hits:
        if str(h).endswith(rel):
            return h
    return None


def extract_archive(src):
    src = Path(src)
    if src.is_dir():
        return src, None
    tmp = Path(tempfile.mkdtemp(prefix='log16-import-v05-run-'))
    with tarfile.open(src, 'r:*') as tar:
        tar.extractall(tmp)
    return tmp, tmp


def locate_pipeline(extracted):
    candidates = list(Path(extracted).rglob('pipeline-output/final-answer.md'))
    if not candidates:
        raise SystemExit('ERROR: pipeline-output/final-answer.md not found')
    return candidates[0].parent


def extract_answer_pattern(final_text):
    m = re.search(r'answer_pattern:\s*([^;\n]+)', final_text)
    if m:
        return m.group(1).strip()
    m = re.search(r'##\s*Тип ответа\s*\n+\s*([^\n]+)', final_text)
    if m:
        return m.group(1).strip()
    return PATTERN_DEFAULT


def extract_section(text, title):
    pattern = rf'##\s*{re.escape(title)}\s*\n(.*?)(?=\n##\s+|\Z)'
    m = re.search(pattern, text, re.S)
    return m.group(1).strip() if m else ''


def extract_top_sources(pipeline_dir, limit=12):
    p = pipeline_dir / 'top-sources.md'
    if not p.exists():
        return []
    sources = []
    for line in read_text(p).splitlines():
        if line.startswith('|') and '`' in line:
            parts = line.split('|')
            if len(parts) >= 5:
                file_part = parts[4] if len(parts) > 4 else ''
                m = re.search(r'`([^`]+)`', line)
                if m:
                    sources.append(m.group(1))
        if len(sources) >= limit:
            break
    # fallback regex
    if not sources:
        for m in re.finditer(r'`(/data/[^`]+)`', read_text(p)):
            sources.append(m.group(1))
            if len(sources) >= limit:
                break
    return sources


def load_summary(pipeline_dir):
    p = pipeline_dir / 'pipeline-summary.json'
    if p.exists():
        try:
            return json.loads(read_text(p))
        except Exception:
            return {}
    return {}


def normalize_answer_pattern(question, pattern, final_text):
    q = (question or '').lower()
    ft = (final_text or '').lower()
    participant_markers = ['участник', 'участника', 'участнику', 'поле деятельности', 'путь участника', 'привлекаемый участник', 'новый участник', 'входной наставник']
    if ('участник' in q or 'участник' in ft) and any(x in q or x in ft for x in ['поле деятельности', 'путь', 'первая задача', 'диагностика', 'входной наставник']):
        return 'participant_pathway'
    return pattern

def detect_gap(final_text, pattern, overall_status):
    low = final_text.lower()
    markers = ['не хватает', 'нет ', 'нужен ', 'нужна ', 'требуется', 'author', 'автор', 'канон', 'needs_author', 'needs review']
    has_gap = overall_status and 'NEEDS_REVIEW' in overall_status
    has_gap = has_gap or any(m in low for m in markers)
    if not has_gap:
        return None
    if 'participant-pathway' in low or 'путь участника' in low or 'участник' in low:
        return {
            'gap_type': 'missing_author_canon',
            'description': 'В ответе выявлен содержательный пробел: требуется авторское/координационное решение и/или канон по теме ответа.',
            'missing_decision': 'Требуется определить и утвердить проектное решение по вопросу.',
            'missing_sources': ['participant-pathway-canon.md'] if 'участник' in low else [],
            'owner': 'author/koordinator',
            'expected_resolution_artifact': 'participant-pathway-canon.md' if 'участник' in low else 'canon-or-status-report.md',
            'status': 'needs_author',
        }
    return {
        'gap_type': 'needs_review_or_source',
        'description': 'Ответ частичный: требуются review, источники или уточняющее решение.',
        'missing_decision': 'Определить, что именно должно быть подтверждено или дооформлено.',
        'missing_sources': [],
        'owner': 'koordinator/archivarius',
        'expected_resolution_artifact': 'review-note-or-status-report.md',
        'status': 'needs_source_review',
    }


def make_task_from_gap(gap, answer_id, pattern, question, stamp):
    return {
        'task_id': f'task__{stamp}__resolve-{pattern}-gap',
        'source_answer_id': answer_id,
        'task_type': 'gap_resolution',
        'owner_entity': gap.get('owner', 'koordinator'),
        'question': f'Закрыть пробел, выявленный по вопросу: {question}',
        'reason': gap.get('description', 'Выявлен пробел в ответе.'),
        'expected_output': gap.get('expected_resolution_artifact', 'review-note.md'),
        'priority': 'high' if gap.get('status') == 'needs_author' else 'normal',
        'status': 'needs_author' if gap.get('status') == 'needs_author' else 'proposed',
        'route_to': ['koordinator', 'consultant'],
        'stop_conditions': ['не переводить ответ в approved_answer до закрытия gap_card'],
    }


def ensure_kernel():
    if not ROOT.exists():
        raise SystemExit(f'ERROR: log16 kernel root not found: {ROOT}')
    for d in [ROOT/'answers'/'needs_review', ROOT/'answers'/'draft', ROOT/'answers'/'approved', ROOT/'gaps'/'detected', ROOT/'tasks'/'proposed', ROOT/'reviews', ROOT/'reports', ROOT/'indexes']:
        d.mkdir(parents=True, exist_ok=True)


def append_jsonl(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')


def main():
    ap = argparse.ArgumentParser(description='Import consultant-pipeline-v05.2 run archive into log16 cards')
    ap.add_argument('run_path', help='Path to v05.2 run archive .tgz or extracted run dir')
    args = ap.parse_args()

    ensure_kernel()
    extracted, tmp = extract_archive(args.run_path)
    try:
        pipeline_dir = locate_pipeline(extracted)
        final = read_text(pipeline_dir / 'final-answer.md')
        summary = load_summary(pipeline_dir)
        question = ''
        qpath = pipeline_dir / 'question.txt'
        if qpath.exists():
            question = read_text(qpath).strip()
        if not question:
            question = summary.get('question', '')
        pattern = normalize_answer_pattern(question, extract_answer_pattern(final), final)
        overall_status = summary.get('overall_status', 'generated')
        answer_status = STATUS_MAP.get(overall_status, 'generated')
        selected_entities = summary.get('selected_entities', []) or []
        top_sources = extract_top_sources(pipeline_dir)
        short_answer = extract_section(final, 'Короткий ответ') or final[:1200]
        limitations = []
        if overall_status != 'FOUND':
            limitations.append(f'pipeline overall_status={overall_status}')
        if not top_sources:
            limitations.append('top_sources not extracted')

        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        date = datetime.datetime.now().isoformat(timespec='seconds')
        slug = re.sub(r'[^a-zA-Z0-9а-яА-Я_-]+', '-', pattern).strip('-').lower() or 'answer'
        answer_id = f'answer__{stamp}__{slug}'
        review_id = f'review__{stamp}__{slug}'

        answer_card = {
            'answer_id': answer_id,
            'question_original': question,
            'question_normalized': question.lower().strip(),
            'answer_pattern': pattern,
            'answer_text': short_answer,
            'source_files': top_sources,
            'selected_entities': selected_entities,
            'status': answer_status,
            'scope': f'imported from consultant run: {Path(args.run_path).name}',
            'limitations': limitations,
            'derived_tasks': [],
            'created_at': date,
            'updated_at': date,
        }

        gap = detect_gap(final, pattern, overall_status)
        created = []
        ans_dir = ROOT/'answers'/'needs_review' if answer_status != 'approved' else ROOT/'answers'/'approved'
        ans_path = ans_dir / f'{answer_id}.json'
        ans_path.write_text(json.dumps(answer_card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        created.append(ans_path)

        gap_id = None
        task_id = None
        if gap:
            gap_id = f'gap__{stamp}__{slug}'
            gap_card = {
                'gap_id': gap_id,
                'source_answer_id': answer_id,
                'gap_type': gap['gap_type'],
                'description': gap['description'],
                'missing_decision': gap.get('missing_decision', ''),
                'missing_sources': gap.get('missing_sources', []),
                'affected_entities': selected_entities,
                'owner': gap.get('owner', 'koordinator'),
                'expected_resolution_artifact': gap.get('expected_resolution_artifact', 'review-note.md'),
                'status': gap.get('status', 'detected'),
            }
            gap_path = ROOT/'gaps'/'detected'/f'{gap_id}.json'
            gap_path.write_text(json.dumps(gap_card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            created.append(gap_path)
            task_card = make_task_from_gap(gap_card, answer_id, pattern, question, stamp)
            task_id = task_card['task_id']
            answer_card['derived_tasks'] = [task_id]
            ans_path.write_text(json.dumps(answer_card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            task_path = ROOT/'tasks'/'proposed'/f'{task_id}.json'
            task_path.write_text(json.dumps(task_card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            created.append(task_path)

        review_card = {
            'review_id': review_id,
            'answer_id': answer_id,
            'review_status': 'accepted_partial' if gap else 'needs_review',
            'reviewer': 'log16-import-v05-run-v01',
            'notes': 'Imported from consultant-pipeline run. Requires human/project review before approval.' if gap else 'Imported from consultant-pipeline run.',
            'accepted_parts': [short_answer[:500]] if short_answer else [],
            'rejected_parts': [] if not gap else ['not approved as final reusable answer until gap is resolved'],
            'created_at': date,
        }
        review_path = ROOT/'reviews'/f'{review_id}.json'
        review_path.write_text(json.dumps(review_card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        created.append(review_path)

        append_jsonl(ROOT/'indexes'/'questions-index.jsonl', {'question': question, 'answer_id': answer_id, 'answer_pattern': pattern, 'status': answer_status})
        append_jsonl(ROOT/'indexes'/'reviews-index.jsonl', {'review_id': review_id, 'answer_id': answer_id, 'review_status': review_card['review_status']})
        if gap_id:
            append_jsonl(ROOT/'indexes'/'gaps-index.jsonl', {'gap_id': gap_id, 'source_answer_id': answer_id, 'status': gap.get('status'), 'owner': gap.get('owner')})
        if task_id:
            append_jsonl(ROOT/'indexes'/'tasks-index.jsonl', {'task_id': task_id, 'source_answer_id': answer_id, 'status': 'needs_author' if gap and gap.get('status') == 'needs_author' else 'proposed'})

        report = ROOT/'reports'/f'import__{stamp}__{slug}.md'
        report.write_text('\n'.join([
            f'# log16 import from run: {Path(args.run_path).name}', '',
            f'Question: {question}', '',
            f'answer_pattern: {pattern}',
            f'overall_status: {overall_status}',
            f'answer_id: {answer_id}',
            f'gap_id: {gap_id or "none"}',
            f'task_id: {task_id or "none"}', '',
            'Created files:',
            *[f'- {p}' for p in created], '',
            'КТО: КОНСУЛЬТАНТ',
            'ДЛЯ ЧЕГО: импорт run v05.2 в log16',
            'СТАТУС: imported_needs_review' if gap else 'СТАТУС: imported',
        ]) + '\n', encoding='utf-8')
        created.append(report)

        print('PASS log16 import completed')
        print(f'ANSWER_CARD: {ans_path}')
        print(f'GAP_CARD: {gap_id or "none"}')
        print(f'TASK_CARD: {task_id or "none"}')
        print(f'REVIEW_CARD: {review_path}')
        print(f'REPORT: {report}')
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__':
    main()
