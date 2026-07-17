# 사뿐 (Sappun) — 소개 사이트

층간소음을 **배려로 풀게 돕는** iOS 앱 **사뿐**의 소개 사이트.

🌙 **https://jsonpassion.github.io/sappun-site/**

사뿐은 소음을 재고 법 기준으로 자동 판정해 기록한다. 배려로 푸는 길(가이드·대화용 자료)을 먼저 안내하고, 그래도 안 풀릴 땐 제출용 자료가 되어 준다. 앱 소스는 별도 비공개 리포에 있고, 이 리포는 **소개 페이지와 법적 문서(개인정보 처리방침·이용약관)** 만 담는다.

## 구성

```
index.html        랜딩 — 히어로(영상) · 공감 · 사용 흐름 4단계 · 기능 · 가격 · FAQ · 마무리
privacy.html      개인정보 처리방침
terms.html        이용약관
style.css         단일 스타일시트 (디자인 토큰 · 스크롤 리빌 · 반응형)
favicon.svg       발자국 파비콘 (+ favicon-32.png, apple-touch-icon.png)
assets/
├── video/        히어로 시네마틱 루프(무음, 720p) + 포스터
└── lottie/       Lottie 8종 (사용 흐름 · 기능)
tools/
└── make-lottie.py  Lottie 전량 재생성 스크립트
```

의존성은 없다. 정적 HTML/CSS + `lottie-web`(CDN) 하나뿐.

## 디자인

컨셉은 앱과 동일한 **"달빛 아래 마루"** — 깊은 밤 위에 달빛 앰버 하나.

- 팔레트 토큰은 `style.css`의 `:root` — 나이트 `#090b12`, 앰버 `#EFA43E`, 크림 `#F5EDD9`
- **악센트는 앰버 하나**. 빨강은 가격의 정상가 취소선처럼 의미가 있을 때만.
- **스크롤 리빌** — `IntersectionObserver`로 `.reveal`(페이드업) / `.reveal-l` · `.reveal-r`(좌우에서 펼쳐짐). 사용 흐름 카드는 단계마다 미디어가 좌↔우로 교차한다. `prefers-reduced-motion`이면 전부 즉시 표시.
- **히어로 영상** — 무음 자동재생 루프 + 포스터. 화면 밖이면 정지하고, 모션 최소화 설정이면 포스터만 보여준다.
- **한글 줄바꿈** — `word-break: keep-all`로 어절 단위로만 끊고(단어 중간 X), 제목은 `text-wrap: balance`. 강제 `<br>`은 짧은 헤드라인에만.

## 로컬 실행

```bash
python3 -m http.server 8931
# → http://localhost:8931
```

## Lottie 재생성

애니메이션은 손으로 만들지 않고 스크립트로 생성한다. 수정은 `tools/make-lottie.py`에서 하고 다시 실행하면 `assets/lottie/*.json`이 전부 갱신된다.

```bash
python3 tools/make-lottie.py
```

같은 파일들이 앱 번들에도 이식되어 있으므로, 팔레트나 모션을 바꾸면 앱 쪽도 함께 갱신할 것.

## 배포

`main`에 푸시하면 GitHub Pages가 자동 배포한다.

## 푸터 표준 (ForgeLab 공통)

```
개인정보 처리방침 · 이용약관 · ✉️ 문의하기(버튼)
© 2026 ForgeLab
ForgeLab · 대표 Jason Lee
```

문의 이메일은 **mailto 버튼 뒤에만** 두고 페이지에 텍스트로 노출하지 않는다.

## 고지

사뿐의 측정값은 스마트폰 마이크로 측정한 참고치로, 「소음·진동 공정시험기준」에 따른 공인 측정을 대체하지 않는다. 앱은 법률 자문을 제공하지 않는다.

---

© 2026 ForgeLab · 대표 Jason Lee
