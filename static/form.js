const $form = document.querySelector(".Cupcake-form");
const $cupcake_ul = document.querySelector(".Cupcake-list");

// TODO: add bootstrap to li
const LI_BOOTSTRAP = "list-group-item d-flex justify-content-between align-items-center";

/**
 * Append all cupcakes from API to the cupcake list
 *
 */
async function display_cupcakes() {
  const resp = await fetch('/api/cupcakes');
  const cupcakes = await resp.json();

  console.log({ cupcakes });

  for (const cupcake of cupcakes["cupcakes"]) {
    const $li = document.createElement("li");
    const $span = document.createElement("span");
    const $img = document.createElement("img");

    // $li.classList.add(LI_BOOTSTRAP)

    const attributes = {flavor: cupcake.flavor, size: cupcake.size, rating: cupcake.rating}

    for (const prop in attributes) {

      const $p = document.createElement("p");

      $p.innerText = `${prop}: ${cupcake[prop]}`;
      $span.append($p);
    }

    $img.src = cupcake.image_url;
    $img.alt = "Cupcake image";

    $li.append($img);
    $li.append($span);

    $cupcake_ul.append($li);
  }
}

/**
 * Start the form
 */
function start() {
  display_cupcakes();
}

export { start };