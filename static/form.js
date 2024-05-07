const $form = document.querySelector(".Cupcake-form");
const $cupcakeUl = document.querySelector(".Cupcake-list");
const $addCupcake = document.querySelector(".Add-cupcake");

// TODO: add bootstrap to li
const LI_BOOTSTRAP = "list-group-item d-flex justify-content-between align-items-center";


/**
 * Get all cupcakes data from the API
 *
 * TODO: show what the data looks like
*/
async function getCupcakes(){
  const resp = await fetch('/api/cupcakes');
  const data = await resp.json();

  console.log("cupcakes data", data.cupcakes);
  return data.cupcakes
}

/**
 * Append all cupcakes from API to the cupcake list
 *
 * Each cupcake is in a <span> inside of a <li>
 * with information about flavor, size, and rating in <p>'s
 * and an <img>.
 *
 * <img> 200 x 200
 */
async function displayCupcakes() {
  const cupcakes = await getCupcakes()

  for (const cupcake of cupcakes) {
    const $li = document.createElement("li");
    const $span = document.createElement("span");
    const $img = document.createElement("img");

    // $li.classList.add(LI_BOOTSTRAP) make this work

    const attributes = {
      flavor: cupcake.flavor,
      size: cupcake.size,
      rating: cupcake.rating
    };

    for (const prop in attributes) {

      const $p = document.createElement("p");

      $p.innerText = `${prop}: ${cupcake[prop]}`;
      $span.append($p);
    }

    $img.src = cupcake.image_url;
    $img.alt = "Cupcake image";
    $img.width = "200";
    $img.height = "200";

    $li.append($img);
    $li.append($span);

    $cupcakeUl.append($li);
  }
}

$addCupcake.addEventListener("click", addCupcakeToAPI);

/**
 * FIXME: Break into 2 functions
 * 1: Get the form data
 * 2: Send to api
 *
 * 3: Create a function to append the saved cupcake to the page, clear out form
 *
 * Add information from cupcake form to the API
 *
 * If nothing is provided for the image_url in the form,
 * the api will have a default image url
 */
async function addCupcakeToAPI(evt) {
  evt.preventDefault()

  const cupcake = {};
  for (const [attr, form_data] of new FormData($form)){
    cupcake[attr] = form_data;
  }
  // if image is '', make it null,
  if(cupcake.image_url === '') cupcake.image_url = null;

  console.log("cupcake to add", cupcake);
  const response = await fetch(`/api/cupcakes`, {
    method: "POST",
    body: JSON.stringify(cupcake),
    headers: {
      "content-type": "application/json",
    },
  });

  // FIXME: return the cupcake data -> await response.json()
}

/**
 * Start the home page
 */
function start() {
  displayCupcakes();
}

export { start };