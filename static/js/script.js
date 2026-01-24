document.addEventListener("DOMContentLoaded", () => {
  const modalEl = document.getElementById("editBookingModal");
  const bodyEl = document.getElementById("editBookingModalBody");

  if (!modalEl || !bodyEl) return;

  const bsModal = new bootstrap.Modal(modalEl);

  async function openEditModal(url) {
    bodyEl.innerHTML = '<p class="text-muted mb-0">Loading…</p>';
    bsModal.show();

    const res = await fetch(url);
    const htmlText = await res.text();

    const doc = new DOMParser().parseFromString(htmlText, "text/html");
    const wrapper = doc.querySelector("#edit-form-wrapper");

    bodyEl.innerHTML = wrapper ? wrapper.innerHTML : "<p>Could not load form.</p>";

    const form = bodyEl.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(form);
      const postRes = await fetch(url, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" }
      });

      if (postRes.ok) {
        window.location.reload();
      } else {
        // if validation errors returned as HTML, re-render form
        const errHtml = await postRes.text();
        const errDoc = new DOMParser().parseFromString(errHtml, "text/html");
        const errWrapper = errDoc.querySelector("#edit-form-wrapper");
        bodyEl.innerHTML = errWrapper ? errWrapper.innerHTML : bodyEl.innerHTML;
      }
    }, { once: true });
  }
   // Edit booking
  document.querySelectorAll(".js-edit-booking").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      openEditModal(btn.dataset.url);
    });
  });
});


