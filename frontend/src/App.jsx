import { useState } from "react";
import { createPublishJob } from "./api";

const initialPublishForm = {
  blogId: "",
  naverUserId: "",
  cookiesRaw: "",
  keyword: ""
};

export default function App() {
  const [publishForm, setPublishForm] = useState(initialPublishForm);
  const [jobResult, setJobResult] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updatePublishForm(event) {
    const { name, value } = event.target;
    setPublishForm((current) => ({ ...current, [name]: value }));
  }

  async function submitPublishJob(event) {
    event.preventDefault();
    setError("");
    setJobResult(null);
    setIsSubmitting(true);

    try {
      const result = await createPublishJob(publishForm);
      setJobResult(result);
    } catch (requestError) {
      setError(`발행 요청에 실패했습니다: ${requestError.message}`);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero">
        <p className="eyebrow">Naver Blog Automation</p>
        <h1>직접 입력한 네이버 세션으로 블로그 포스팅 자동화</h1>
        <p className="hero-copy">
          로그인된 브라우저에서 추출한 cookiesRaw와 blogId, naverUserId를 넣으면 백엔드가 Python 발행기를 호출합니다.
        </p>
      </section>

      {error ? <section className="panel error">{error}</section> : null}

      <section className="grid single-column">
        <form className="panel" onSubmit={submitPublishJob}>
          <div className="panel-header">
            <h2>발행 정보 입력</h2>
            <p>지금은 계정 저장 단계 없이 입력값으로 바로 포스팅 요청을 보냅니다.</p>
          </div>

          <label>
            Blog ID
            <input name="blogId" value={publishForm.blogId} onChange={updatePublishForm} required />
          </label>

          <label>
            Naver User ID
            <input name="naverUserId" value={publishForm.naverUserId} onChange={updatePublishForm} required />
          </label>

          <label>
            Keyword
            <input name="keyword" value={publishForm.keyword} onChange={updatePublishForm} required />
          </label>

          <label>
            cookiesRaw
            <textarea
              name="cookiesRaw"
              value={publishForm.cookiesRaw}
              onChange={updatePublishForm}
              rows="10"
              required
            />
          </label>

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "발행 요청 중..." : "블로그 포스팅 실행"}
          </button>
        </form>

        {jobResult ? (
          <section className="panel job-result">
            <h3>실행 결과</h3>
            <p>Status: {jobResult.status}</p>
            <p>Blog ID: {jobResult.blogId}</p>
            <p>Naver User ID: {jobResult.naverUserId}</p>
            <p>Keyword: {jobResult.keyword}</p>
            <p>Message: {jobResult.message}</p>
            {jobResult.publishUrl ? <p>Publish URL: {jobResult.publishUrl}</p> : null}
          </section>
        ) : null}
      </section>
    </main>
  );
}
