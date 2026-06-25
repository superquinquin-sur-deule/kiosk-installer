(function () {
  const btn = document.createElement("div");
  btn.className = "oe_status";
  btn.innerHTML =
    '<div class="oe_icon">' +
    '<i class="fa fa-fw fa-refresh" aria-label="Rafraîchir" title="Rafraîchir"></i>' +
    "</div>";
  btn.addEventListener("click", () => location.reload());

  const observer = new MutationObserver(() => {
    const target = document.querySelector(".pos-topheader .header-button");
    if (!target) return;

    target.style.display = "none";
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        target.style.display =
          target.style.display === "none" ? "block" : "none";
      }
    });

    target.insertAdjacentElement("beforebegin", btn);
    observer.disconnect();
  });

  observer.observe(document.body, { childList: true, subtree: true });
})();
