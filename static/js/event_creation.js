
document.addEventListener("DOMContentLoaded", function () {
  const addBtn   = document.getElementById("add-image");
  const formsDiv = document.getElementById("images-forms");
  const emptyTpl = document.getElementById("empty-form");
  if (!addBtn || !formsDiv || !emptyTpl) return;


  const mgmt = formsDiv.parentElement.querySelector('input[name$="-TOTAL_FORMS"]');
  if (!mgmt) return;


  const SUFFIX = "-TOTAL_FORMS";
  const prefix = mgmt.name.endsWith(SUFFIX) ? mgmt.name.slice(0, -SUFFIX.length) : mgmt.name;
  const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`) || mgmt;


  formsDiv.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach(chk => (chk.style.display = "none"));


  function attachRemove(block, isFirst) {
    if (isFirst) return;


    if (block.querySelector(".remove-image")) return;

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Remove";
    btn.className = "remove-image";

    btn.addEventListener("click", function () {

      const del = block.querySelector('input[type="checkbox"][name$="-DELETE"]');
      if (del) del.checked = true;


      block.style.display = "none";
    });

    block.appendChild(btn);
  }


  const initialBlocks = Array.from(formsDiv.querySelectorAll(".track-image-form"));
  initialBlocks.forEach((blk, idx) => {

    blk.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach(chk => (chk.style.display = "none"));
    attachRemove(blk, idx === 0);
  });


  addBtn.addEventListener("click", function () {
    const index = Number(totalForms.value);  // следващият индекс
    const html  = emptyTpl.innerHTML.replaceAll("__prefix__", String(index));

    const t = document.createElement("template");
    t.innerHTML = html.trim();
    const node = t.content.firstElementChild;


    node.querySelectorAll('input[type="file"]').forEach(inp => inp.value = "");
    node.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], textarea')
        .forEach(inp => inp.value = "");


    node.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach(chk => (chk.style.display = "none"));

    formsDiv.appendChild(node);


    attachRemove(node, false);


    totalForms.value = String(index + 1);
  });
});
