document.addEventListener("DOMContentLoaded", () => {
  // Improve form usability and prevent accidental double submission.
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector('button[type="submit"]');
      if (button && !button.disabled && !form.classList.contains("quantity-form")) {
        button.dataset.originalText = button.textContent;
        // Keep the original label visible; server-side validation remains authoritative.
      }
    });
  });

  // Dismiss status messages after a short delay.
  document.querySelectorAll(".message").forEach((message) => {
    window.setTimeout(() => {
      message.classList.add("message-hide");
    }, 5000);
  });
});
