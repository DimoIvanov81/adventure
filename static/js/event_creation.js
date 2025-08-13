// static/js/event_form.js
document.addEventListener("DOMContentLoaded", function () {
  const addBtn   = document.getElementById("add-image");
  const formsDiv = document.getElementById("images-forms");
  const emptyTpl = document.getElementById("empty-form");
  if (!addBtn || !formsDiv || !emptyTpl) return;

  // намери management input-а за TOTAL_FORMS (какъвто и да е префиксът)
  const mgmt = formsDiv.parentElement.querySelector('input[name$="-TOTAL_FORMS"]');
  if (!mgmt) return;

  // изведи prefix-а без regex
  const SUFFIX = "-TOTAL_FORMS";
  const prefix = mgmt.name.endsWith(SUFFIX) ? mgmt.name.slice(0, -SUFFIX.length) : mgmt.name;
  const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`) || mgmt;

  // скрий всички DELETE чекбоксове, ако са рендерирани
  formsDiv.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach(chk => (chk.style.display = "none"));

  // добавя визуален Remove бутон към даден блок (НЕ за първия)
  function attachRemove(block, isFirst) {
    if (isFirst) return; // първата форма не се маха

    // не добавяй втори remove, ако вече има
    if (block.querySelector(".remove-image")) return;

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Remove";
    btn.className = "remove-image";

    btn.addEventListener("click", function () {
      // намери скрития DELETE чекбокс вътре и го чекни
      const del = block.querySelector('input[type="checkbox"][name$="-DELETE"]');
      if (del) del.checked = true;

      // скрий визуално блока (оставяме го в DOM, за да подадем DELETE към Django)
      block.style.display = "none";
    });

    block.appendChild(btn);
  }

  // инициализация: добави Remove бутон на всички форми след първата
  const initialBlocks = Array.from(formsDiv.querySelectorAll(".track-image-form"));
  initialBlocks.forEach((blk, idx) => {
    // скрий DELETE чекбоксовете вътре, ако са видими
    blk.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach(chk => (chk.style.display = "none"));
    attachRemove(blk, idx === 0);
  });

  // добавяне на нова форма (без regex, без reindex)
  addBtn.addEventListener("click", function () {
    const index = Number(totalForms.value);  // следващият индекс
    const html  = emptyTpl.innerHTML.replaceAll("__prefix__", String(index));

    const t = document.createElement("template");
    t.innerHTML = html.trim();
    const node = t.content.firstElementChild;

    // изчисти стойности
    node.querySelectorAll('input[type="file"]').forEach(inp => inp.value = "");
    node.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], textarea')
        .forEach(inp => inp.value = "");

    // скрий DELETE чекбокса, ако го има
    node.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach(chk => (chk.style.display = "none"));

    formsDiv.appendChild(node);

    // този нов блок НЕ е първият -> добавяме Remove
    attachRemove(node, false);

    // увеличаваме TOTAL_FORMS (само това!)
    totalForms.value = String(index + 1);
  });
});
