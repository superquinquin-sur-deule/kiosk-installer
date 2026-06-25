(function () {
  "use strict";

  document.addEventListener(
    "click",
    function (event) {
      const target = event.target;
      if (
        target &&
        target.tagName === "A" &&
        target.href &&
        target.href.startsWith("blob:")
      ) {
        event.preventDefault();
        event.stopPropagation();
      }
    },
    true,
  );
})();
