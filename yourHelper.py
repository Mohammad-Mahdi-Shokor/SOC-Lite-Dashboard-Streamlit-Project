import streamlit as st
from pathlib import Path
import sys
import json
from collections import Counter

# Ensure the project root (parent of this folder) is on sys.path so imports
# like `llm_deepseek` and `llm_gemini` (located in the workspace root) resolve.
current_dir = Path(__file__).parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from llm_deepseek import AskDeepSeek
from llm_gemini import chatWithGemini


def _load_json_data(filename: str):
	p = Path(__file__).with_name(filename)
	if not p.exists():
		return []
	try:
		return json.loads(p.read_text(encoding="utf-8"))
	except Exception:
		return []


def _is_soc_scope_query(user_message: str) -> bool:
	text = user_message.lower()
	allowed_keywords = [
		"report", "reports", "reporter", "reporters", "incident", "incidents",
		"alert", "alerts", "severity", "critical", "high", "medium", "low",
		"threat", "vulnerability", "sqli", "xss", "ddos", "ransomware", "phishing",
		"target", "affected", "trend", "dashboard", "soc"
	]
	return any(k in text for k in allowed_keywords)


def _build_soc_context(max_recent: int = 30) -> str:
	reports = _load_json_data("reports.json")
	reporters = _load_json_data("reporters.json")

	if not isinstance(reports, list):
		reports = []
	if not isinstance(reporters, list):
		reporters = []

	reporter_names = [str(r.get("name", "")).strip() for r in reporters if isinstance(r, dict) and r.get("name")]

	severity_counter = Counter()
	type_counter = Counter()
	target_counter = Counter()

	for row in reports:
		if not isinstance(row, dict):
			continue
		severity = str(row.get("severity", "Unknown")).strip() or "Unknown"
		r_type = str(row.get("type", "Unknown")).strip() or "Unknown"
		severity_counter[severity] += 1
		type_counter[r_type] += 1
		for t in row.get("affectedTargets", []) if isinstance(row.get("affectedTargets"), list) else []:
			target_counter[str(t)] += 1

	recent_reports = sorted(
		[r for r in reports if isinstance(r, dict)],
		key=lambda x: str(x.get("time", "")),
		reverse=True
	)[:max_recent]

	def _fmt_counter(counter_obj: Counter, top_n: int = 8) -> str:
		if not counter_obj:
			return "none"
		return ", ".join([f"{k}: {v}" for k, v in counter_obj.most_common(top_n)])

	recent_lines = []
	for r in recent_reports:
		recent_lines.append(
			f"- {r.get('time', 'unknown-date')} | reporter={r.get('name', 'unknown')} | "
			f"type={r.get('type', 'unknown')} | severity={r.get('severity', 'unknown')} | "
			f"targets={', '.join(r.get('affectedTargets', [])) if isinstance(r.get('affectedTargets'), list) else 'none'}"
		)

	return (
		"SOC DATA CONTEXT\n"
		f"- Total reports: {len(reports)}\n"
		f"- Total reporters: {len(reporter_names)}\n"
		f"- Reporter names: {', '.join(reporter_names) if reporter_names else 'none'}\n"
		f"- Severity distribution: {_fmt_counter(severity_counter)}\n"
		f"- Top incident types: {_fmt_counter(type_counter)}\n"
		f"- Most affected targets: {_fmt_counter(target_counter)}\n"
		"- Recent reports:\n"
		+ ("\n".join(recent_lines) if recent_lines else "- none")
	)


def _build_scoped_prompt(user_message: str) -> str:
	soc_context = _build_soc_context()
	return (
		"You are a SOC dashboard assistant.\n"
		"Rules:\n"
		"1) Answer ONLY using report/reporters data provided below.\n"
		"2) If the question is outside SOC reports scope, refuse briefly and redirect to report-related queries.\n"
		"3) Be concise and factual; if data is missing, say so.\n\n"
		f"{soc_context}\n\n"
		f"User question: {user_message}\n"
	)


def load_policy_text():
	p = Path(__file__).with_name("AI_POLICY.md")
	if p.exists():
		return p.read_text(encoding="utf-8")
	return "No policy found."


def get_ai_response(user_message: str) -> str:
	"""Mock AI response function.

	Replace this with your real model call. This function follows the policy by
	returning safe defaults for disallowed content.
	"""
	text = user_message.lower()
	# Simple safety checks
	disallowed_keywords = ["kill", "bomb", "suicide", "hack", "illegal"]
	if any(k in text for k in disallowed_keywords):
		return ("I can’t help with that. If you need assistance with safety or legal matters, please consult appropriate professionals."
		)

	if not _is_soc_scope_query(user_message):
		return "I can help only with SOC dashboard reports and reporters data. Ask about incidents, severities, trends, affected targets, or reporter activity."

	# Simple canned responses for demo
	if "hello" in text or "hi" in text:
		return "Hello — how can I help you today?"
	if "help" in text:
		return "Tell me what you need help with and I’ll do my best to assist."

	return chatWithGemini(_build_scoped_prompt(user_message))


def getDeepseekResponse(user_message: str) -> str:
	"""Mock AI response function.

	Replace this with your real model call. This function follows the policy by
	returning safe defaults for disallowed content.
	"""
	text = user_message.lower()
	# Simple safety checks
	disallowed_keywords = ["kill", "bomb", "suicide", "hack", "illegal"]
	if any(k in text for k in disallowed_keywords):
		return ("I can’t help with that. If you need assistance with safety or legal matters, please consult appropriate professionals."
		)

	if not _is_soc_scope_query(user_message):
		return "I can help only with SOC dashboard reports and reporters data. Ask about incidents, severities, trends, affected targets, or reporter activity."

	# # Simple canned responses for demo
	# if "hello" in text or "hi" in text:
	# 	return "Hello — how can I help you today?"
	# if "help" in text:
	# 	return "Tell me what you need help with and I’ll do my best to assist."

	return AskDeepSeek(_build_scoped_prompt(user_message))