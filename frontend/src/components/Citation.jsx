// Renders a single citation tag, e.g. "[Smart_Hire.pdf, Page 3]"
// Styled like a highlighter mark on paper — the signature visual element tying back to DocuMind's core feature: grounded, traceable answers.
function Citation({ filename, page }) {
  return (
    <span className="inline-block font-mono text-xs text-[#1C1B1A] bg-[#FFD84D] px-1.5 py-0.5 rounded mr-1.5 mb-1">
      {filename}, p.{page}
    </span>
  )
}

export default Citation