# pyright: reportMissingImports=false
import os
import sys
from typing import Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

import gradio as gr  # type: ignore
from gradio.themes import Base as GradioTheme

from browser_use import Agent, ChatGoogle, ChatGroq, ChatOllama
from browser_use.browser import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.llm import BaseChatModel

FREE_MODELS: dict[str, tuple[str, str, bool]] = {
	'Ollama · llama3.1:8b (محلی و رایگان)': ('ollama', 'llama3.1:8b', False),
	'Ollama · llama3.2:3b (محلی، سبک و رایگان)': ('ollama', 'llama3.2:3b', False),
	'Gemini · gemini-2.5-flash (سهمیه رایگان)': ('google', 'gemini-2.5-flash', True),
	'Gemini · gemini-2.5-flash-lite (سهمیه رایگان)': ('google', 'gemini-2.5-flash-lite', True),
	'Groq · gpt-oss-20b (سهمیه رایگان)': ('groq', 'openai/gpt-oss-20b', False),
	'Groq · Llama 4 Scout (سهمیه رایگان)': ('groq', 'meta-llama/llama-4-scout-17b-16e-instruct', True),
}
DEFAULT_FREE_MODEL = 'Ollama · llama3.1:8b (محلی و رایگان)'

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap');

:root { color-scheme: dark; }
* { box-sizing: border-box; }
body, .gradio-container {
  background: #101112 !important;
  color: #e7e7e7 !important;
  font-family: 'Vazirmatn', system-ui, sans-serif !important;
}
.gradio-container { max-width: none !important; padding: 0 !important; }
#app-shell {
  min-height: 100vh;
  padding-bottom: 36px;
  direction: rtl;
  background: radial-gradient(ellipse at 50% -18%, #252a29 0, #141616 34%, #101112 68%);
}
#topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 0 28px;
  border-bottom: 1px solid #303333;
  background: rgba(17, 18, 19, .92);
  backdrop-filter: blur(18px);
}
.topbar-inner {
  max-width: 1180px;
  min-height: 66px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  direction: ltr;
}
.header-leading, .header-actions, .browser-pill { display: inline-flex; align-items: center; gap: 12px; }
.header-leading, .header-actions { direction: rtl; }
.header-icon { width: 34px; height: 34px; display: grid; place-items: center; border: 1px solid #3d4240; border-radius: 11px; color: #b7bfbb; }
.page-title { color: #d6d8d7; font-size: 14px; white-space: nowrap; }
.browser-pill {
  padding: 7px 12px;
  border: 1px solid #343a38;
  border-radius: 999px;
  color: #b9c0bd;
  font-size: 12px;
}
.browser-led { width: 8px; height: 8px; border-radius: 50%; background: #25c49a; box-shadow: 0 0 12px #25c49a55; }
#workspace { width: min(100%, 940px); margin: 0 auto; padding: 24px 26px 0; }
#session-strip {
  display: flex; align-items: center; justify-content: space-between; gap: 14px;
  margin-bottom: 18px; padding: 12px 15px;
  border: 1px solid #292e2c; border-radius: 15px;
  background: #161918; color: #aab2ae;
}
.session-label { display: flex; align-items: center; gap: 9px; font-size: 13px; }
.session-caption { color: #777f7b; font-size: 12px; }
#run-status { margin: 0 !important; color: #929a96 !important; font-size: 12px !important; }
#welcome { margin: 26px 0 8px; color: #858d89; font-size: 13px; text-align: center; }
#chatbot { background: transparent !important; border: 0 !important; box-shadow: none !important; }
#chatbot .wrap, #chatbot .panel { background: transparent !important; border: 0 !important; box-shadow: none !important; }
#chatbot .message { border-radius: 18px !important; line-height: 1.85 !important; }
#composer {
  position: sticky; bottom: 12px; z-index: 5;
  margin-top: 12px; padding: 13px 15px 10px;
  border: 1px solid #3a3e3d; border-radius: 24px;
  background: rgba(31, 32, 32, .96); box-shadow: 0 18px 60px #0007;
}
#composer-input textarea {
  min-height: 64px !important; padding: 10px 7px !important;
  border: 0 !important; background: transparent !important; color: #ededed !important;
  font-family: inherit !important; font-size: 15px !important; line-height: 1.8 !important;
  box-shadow: none !important; direction: rtl !important;
}
#composer-input textarea::placeholder { color: #858b89 !important; }
#composer-toolbar { align-items: center; justify-content: space-between; }
#toolbar-right, #toolbar-left { align-items: center; gap: 9px; }
#file-upload button {
  min-height: 38px !important; padding: 0 12px !important;
  border: 1px solid #3c4140 !important; border-radius: 13px !important;
  background: #262928 !important; color: #c6ceca !important; font-family: inherit !important;
}
#settings { border: 0 !important; background: transparent !important; }
#settings > div:first-child { padding: 7px 10px !important; color: #9ba29f !important; font-size: 12px !important; }
#settings .wrap { border-color: #383d3b !important; border-radius: 14px !important; background: #202322 !important; }
#settings label, #settings input, #settings select { font-family: inherit !important; }
#model { min-width: 170px; max-width: 230px; }
#api-key, #ollama-host, #headless { min-width: 130px; }
#model .wrap, #model [role="combobox"] { border-color: #3c4140 !important; border-radius: 13px !important; background: #262928 !important; color: #c6ceca !important; }
#send-button {
  min-width: 82px !important; min-height: 42px !important;
  border: 0 !important; border-radius: 14px !important;
  background: #f1f3f2 !important; color: #171a19 !important;
  font-family: inherit !important; font-weight: 700 !important;
}
#send-button:hover { background: #dce4e0 !important; }
.footer-note { margin: 10px 6px 0; color: #626966; font-size: 11px; text-align: center; }
@media (max-width: 680px) {
  #topbar { padding: 0 14px; }
  .topbar-inner { min-height: 58px; gap: 8px; }
  .header-leading, .header-actions { gap: 8px; }
  .page-title { font-size: 13px; }
  #workspace { padding: 14px 12px 0; }
  #session-strip { margin-bottom: 12px; padding: 10px 12px; }
  .session-caption { display: none; }
  #chatbot { min-height: 48vh; }
  #composer { bottom: 6px; margin-top: 8px; padding: 10px 11px 8px; border-radius: 21px; }
  #composer-input textarea { min-height: 54px !important; font-size: 14px !important; }
  #file-upload button { min-height: 36px !important; padding: 0 10px !important; }
  #send-button { min-width: 68px !important; min-height: 38px !important; }
}
"""


async def run_browser_task(
	task: str,
	history: list[dict[str, Any]] | None,
	model_choice: str,
	api_key: str,
	ollama_host: str,
	headless: bool,
	files: list[str] | None,
):
	messages = list(history or [])
	if not task.strip():
		yield messages, 'ابتدا کار موردنظر را بنویسید.', task, files
		return

	uploaded_files = [str(path) for path in (files or [])]
	user_message = task
	if uploaded_files:
		file_names = ', '.join(os.path.basename(path) for path in uploaded_files)
		user_message += f'\n\nپیوست‌ها: {file_names}'
	messages.extend(
		[
			{'role': 'user', 'content': user_message},
			{'role': 'assistant', 'content': 'در حال اجرای مراحل در مرورگر...'},
		]
	)
	try:
		llm = create_free_model(model_choice, api_key, ollama_host)
	except ValueError as e:
		messages[-1]['content'] = str(e)
		yield messages, 'تنظیم مدل لازم است', task, files
		return

	yield messages, 'در حال اجرا', '', None
	try:
		browser_session = create_browser_session(headless)
		agent = Agent(
			task=task,
			llm=llm,
			browser_session=browser_session,
			available_file_paths=uploaded_files,
			use_vision=FREE_MODELS[model_choice][2],
		)
		result = await agent.run()
		if not result.is_done() or result.is_successful() is False:
			errors = [error for error in result.errors() if error]
			messages[-1]['content'] = errors[-1] if errors else 'عامل نتوانست موفقیت کار را تأیید کند.'
			yield messages, 'اجرا با خطا متوقف شد', '', None
			return
		messages[-1]['content'] = result.final_result() or 'کار تمام شد.'
		yield messages, 'انجام شد', '', None
	except Exception as e:
		messages[-1]['content'] = f'خطا در اجرای کار: {e}'
		yield messages, 'اجرا با خطا متوقف شد', '', None


def create_free_model(model_choice: str, api_key: str, ollama_host: str) -> BaseChatModel:
	provider, model, _supports_vision = FREE_MODELS[model_choice]
	if provider == 'ollama':
		host = (ollama_host or os.getenv('OLLAMA_HOST', '')).strip() or None
		return ChatOllama(model=model, host=host)

	if provider == 'google':
		key = (api_key or os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY') or '').strip()
		if not key:
			raise ValueError('برای Gemini یک کلید رایگان Google وارد کنید یا از Ollama محلی استفاده کنید.')
		return ChatGoogle(model=model, api_key=key)

	key = (api_key or os.getenv('GROQ_API_KEY', '')).strip()
	if not key:
		raise ValueError('برای Groq یک کلید رایگان وارد کنید یا از Ollama محلی استفاده کنید.')
	return ChatGroq(model=model, api_key=key)


def create_browser_profile(headless: bool) -> BrowserProfile:
	return BrowserProfile(headless=headless, user_data_dir=None)


def create_browser_session(headless: bool) -> BrowserSession:
	cdp_url = os.getenv('BROWSER_USE_CDP_URL', '').strip()
	if cdp_url:
		return BrowserSession(cdp_url=cdp_url)
	return BrowserSession(browser_profile=create_browser_profile(headless))


def create_ui():
	with gr.Blocks(
		title='Browser Use | دستیار مرورگر',
	) as interface:
		with gr.Column(elem_id='app-shell'):
			gr.HTML(
				"""
				<header class="topbar-inner">
				  <div class="header-leading">
				    <span class="header-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="7" height="16" rx="1"/><rect x="14" y="4" width="7" height="16" rx="1"/></svg></span>
				    <div class="page-title">دستیار مرورگر</div>
				  </div>
				  <div class="header-actions">
				    <span class="header-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 15V3m0 0L7 8m5-5 5 5M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/></svg></span>
				    <div class="browser-pill"><span>Browser</span><span class="browser-led"></span></div>
				  </div>
				</header>
				""",
				elem_id='topbar',
			)
			with gr.Column(elem_id='workspace'):
				with gr.Row(elem_id='session-strip'):
					gr.HTML('<div class="session-label"><span class="browser-led"></span><span>آماده برای اجرای کار</span></div>')
					status = gr.Markdown('آماده', elem_id='run-status')
				gr.Markdown('کار وب را توضیح دهید؛ عامل آن را در مرورگر انجام می‌دهد.', elem_id='welcome')
				chat = gr.Chatbot(
					value=[{'role': 'assistant', 'content': 'سلام. چه کاری را در مرورگر انجام بدهم؟'}],
					show_label=False,
					height=480,
					rtl=True,
					layout='bubble',
					elem_id='chatbot',
				)
				with gr.Column(elem_id='composer'):
					task = gr.Textbox(
						show_label=False,
						lines=2,
						max_lines=5,
						placeholder='پیام را بنویسید...',
						elem_id='composer-input',
					)
					with gr.Accordion('تنظیمات مدل و مرورگر', open=False, elem_id='settings'):
						gr.Markdown(
							'برای استفاده بدون هزینهٔ API، Ollama را نصب کنید و یک‌بار `ollama pull llama3.1:8b` را اجرا کنید. '
							'سهمیهٔ رایگان Gemini و Groq محدود است و ممکن است تغییر کند.'
						)
						api_key = gr.Textbox(
							label='کلید Gemini یا Groq (برای Ollama لازم نیست)',
							placeholder='کلید حساب رایگان خود را وارد کنید',
							type='password',
							elem_id='api-key',
						)
						ollama_host = gr.Textbox(
							label='نشانی Ollama محلی',
							value=os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
							elem_id='ollama-host',
						)
						headless = gr.Checkbox(label='اجرای بدون نمایش پنجره مرورگر', value=True, elem_id='headless')
					with gr.Row(elem_id='composer-toolbar'):
						with gr.Row(elem_id='toolbar-right'):
							files = gr.UploadButton('پیوست فایل', file_count='multiple', type='filepath', elem_id='file-upload')
							model = gr.Dropdown(
								choices=list(FREE_MODELS),
								label=None,
								value=DEFAULT_FREE_MODEL,
								container=False,
								elem_id='model',
							)
						with gr.Row(elem_id='toolbar-left'):
							submit = gr.Button('اجرا', variant='primary', elem_id='send-button')
				gr.Markdown(
					'Ollama محلی به کلید نیاز ندارد؛ کلید Gemini/Groq فقط برای همان اجرا استفاده می‌شود.',
					elem_id='footer-note',
					elem_classes=['footer-note'],
				)

			inputs = [task, chat, model, api_key, ollama_host, headless, files]
			outputs = [chat, status, task, files]
			submit.click(fn=run_browser_task, inputs=inputs, outputs=outputs)
			task.submit(fn=run_browser_task, inputs=inputs, outputs=outputs)

	return interface


if __name__ == '__main__':
	theme = GradioTheme(primary_hue='emerald', neutral_hue='slate').set(
		body_background_fill='#101112',
		body_text_color='#e7e7e7',
		background_fill_primary='#161918',
		background_fill_secondary='#202322',
		block_border_color='#303534',
		input_background_fill='#1f2020',
		input_border_color='#3a3e3d',
	)
	create_ui().queue().launch(theme=theme, css=CSS)
