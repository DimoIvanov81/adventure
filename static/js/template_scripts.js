document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.getElementById("add-image");
  const formsDiv = document.getElementById("images-forms");
  const emptyForm = document.getElementById("empty-form");
  const totalForms = document.getElementById("id_images-TOTAL_FORMS");



  let formCount = parseInt(totalForms.value);

  addBtn.addEventListener("click", function () {
    const wrapper = document.createElement("div");
    wrapper.classList.add("track-image-form");

    const html = emptyForm.innerHTML.replaceAll("__prefix__", formCount.toString());
    const template = document.createElement("template");
    template.innerHTML = html.trim();

    const newForm = template.content.firstChild;


    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.textContent = "Remove";
    removeBtn.classList.add("remove-image", "btn", "btn-danger", "mt-2");


    removeBtn.addEventListener("click", function () {
      wrapper.remove();
      formCount--;
      totalForms.value = formCount.toString();
    });

    newForm.appendChild(removeBtn);
    wrapper.appendChild(newForm);
    formsDiv.appendChild(wrapper);

    formCount++;
    totalForms.value = formCount.toString();
  });
});
