const BASE_URL = "http://127.0.0.1:5000/api";

// Create cupcake list html
function createHTMLCupcakeList(cupcake) {
    return `
    <div class="container">
        <li cupcake-data-id=${ cupcake.id }>
            <img class="cupcake-photo" src=${ cupcake.image }  width='200' height='200'> 
            <p>Flavor: ${ cupcake.flavor }</p> 
            <p>Size: ${ cupcake.size }</p>
            <p>Rating: ${ cupcake.rating }</p>
            <button class="delete-cupcake" data-id="${ cupcake.id }">Delete</button>
        </li>
    </div>
    `;  
}

// Create function that shows existing cupcakes
async function showExistingCupcakes() {
    let response = await axios.get(`${BASE_URL}/cupcakes`);
    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = createHTMLCupcakeList(cupcakeData);
        $('#listed-cupcakes').append(newCupcake);
    };
};

// Handle adding cupcake form
$("#create-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
  
    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();
  
    const newCreatedCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {flavor, size, rating, image});
  
    let newCupcake = $(createHTMLCupcakeList(newCreatedCupcakeResponse.data.cupcake));
    $("#listed-cupcakes").append(newCupcake);
    $("#create-cupcake-form").trigger("reset");
  });

$("#listed-cupcakes").on("click", ".delete-cupcake", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("cupcake-data-id");
  
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
  });

$(showExistingCupcakes);