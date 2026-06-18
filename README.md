# Taygido Bot

타기도 봇은 Ollama 기반의 디스코드 AI 챗봇입니다! (비록 타기 타기도 같은 말 밖에 못하지만...)

"타기도"를 부르거나 봇을 멘션하면 메시지를 분석하고, 친밀도를 기록하며 응답을 생성합니다!

## 주요 기능

* Ollama 기반 AI 응답 생성
* 사용자 친밀도 시스템
* 감정 분석
* 질문 여부 판별
* 랜덤 이모지 반응
* 친밀도 랭킹
* Discord Slash Command 지원

---

## 필요 환경

### Python

* Python 3.10 이상 권장

### 필수 패키지

```bash
pip install -r requirements.txt
```

### Ollama

이 프로젝트는 로컬에서 실행되는 Ollama를 사용합니다!

먼저 Ollama를 설치한 후 아래 명령어로 모델을 다운로드하세요.

```bash
ollama pull llama3:8b
```

모델 다운로드 후 Ollama를 실행합니다.

```bash
ollama serve
```

현재 기본 설정 모델:

```python
OLLAMA_MODEL = "llama3:8b"
```

---

## 설치 방법

### 저장소 복제

```bash
git clone https://github.com/rweincat/taygido-bot.git

cd taygido-bot
```

### 패키지 설치

```bash
pip install -r requirements.txt
```

---

## Discord Bot 생성 (없다면!)

1. Discord Developer Portal 접속
2. 새 애플리케이션 생성
3. Bot 메뉴에서 봇 생성
4. Token 복사

---

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```env
TOKEN=YOUR_DISCORD_BOT_TOKEN
```

예시

```env
TOKEN=MTExMTExMTExMTExMTEx...
```

보안상 실제 토큰은 절대절대 외부에 유출하지 마세요!

## 실행 방법

먼저 Ollama를 실행합니다.

```bash
ollama serve
```

그 후 봇을 실행합니다.

```bash
python bot.py
```

정상적으로 실행되면 다음과 비슷한 로그가 출력됩니다.

```text
[READY] Logged in as Taygi
[SYNC] 2 slash commands synced
```

---

## 동작 방식

봇은 다음 경우에 반응합니다.

* 메시지에 "타기"가 포함된 경우
* 타기도가 멘션된 경우

메시지를 분석하여

* 긍정/부정 감정
* 욕설 여부
* 질문 여부
* 애정 표현 여부

등을 판단합니다.

분석 결과에 따라 친밀도가 증가하거나 감소할 수 있습니다.

---

## 친밀도 시스템

사용자의 말에 따라 친밀도가 변합니다.

예시

* 칭찬
* 애정 표현
* 긍정적인 대화

→ 친밀도 증가

반대로

* 욕설
* 공격적인 표현
* 부정적인 대화

→ 친밀도 감소

응답 하단에 변화량이 표시될 수 있습니다.

예시

```text
♥️+3
```

또는

```text
💔-5
```

---

## 슬래시 명령어

### /affinity

현재 자신의 친밀도를 확인합니다.

### /ranking

친밀도 랭킹을 확인합니다.

---

## 프로젝트 구조

```text
taygido-bot/
│
├── bot.py
├── config.py
├── requirements.txt
│
├── commands/
│   ├── affinity_cmd.py
│   └── ranking_cmd.py
│
├── core/
│   ├── affinity.py
│   ├── emotions.py
│   ├── rarity.py
│   ├── responder.py
│   └── event/
│       └── self_destruct.py
│
├── llm/
│   ├── analyzer.py
│   └── ollama_client.py
│
├── data/
│   ├── affinity.json
│   └── memory.json
│
└── utils/
```

---

## 주의 사항

* Ollama가 실행 중이지 않으면 응답을 생성할 수 없습니다.
* Discord Bot Token은 절대 공개하지 마세요.
* 개인 학습 및 취미 목적으로 제작된 프로젝트입니다.

---

## 라이선스

MIT License

자유롭게 사용, 수정, 배포할 수 있습니다.
