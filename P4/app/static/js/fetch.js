var recetas = []              // declaraciones   
fetchApp('/api/recipes');
if (localStorage.getItem('fontSize')==null){
  let actualValue = document.getElementById('fontDiv').style.fontSize;
  let value = actualValue.substring(0,actualValue.length-3);
  localStorage.setItem('fontSize',value);
}
document.getElementById('fontDiv').style.fontSize = localStorage.getItem('fontSize')+'rem';

if (localStorage.getItem('mode')==null){
  localStorage.setItem('mode','day');
}
changeMode();

// fetch devuelve una promise
function fetchApp(url){

  let html_str  = ''              // de variables
  let i         = 0               //
  recetas=[];

  fetch(url)           // GET por defecto,
  .then(res => res.json())        // respuesta en json, otra promise
  .then(filas => {                // arrow function
      filas.forEach(fila => {     // bucle ES6, arrow function
          i++
          recetas.push(fila)      // se guardan para después sacar cada una  
          // ES6 templates
          html_str += ` <tr>
                        <td>${i}</td>
                        <td>
                            <button onclick="detalle('${i}')" 
                                  type="button" class="btn btn-outline btn-sm"
                                  data-bs-toggle="modal" data-bs-target="#detailModal"
                                  style="font-size: inherit; color: inherit">
                            ${fila.name}
                            </button>
                          </td>
                          <td>
                            <button onclick="showEditModal('${i}')"
                                    type="button" class="btn btn-warning btn-sm"
                                    data-bs-toggle="modal" data-bs-target="#formModal"
                                    style="font-size: inherit;">
                            Edit
                            </button>
                            <button onclick="showDeleteModal('${i}')"
                                    type="button" class="btn btn-danger btn-sm"
                                    data-bs-toggle="modal" data-bs-target="#deleteModal"
                                    style="font-size: inherit;">
                            Delete
                            </button>
                          </td>
                        </tr>`         // ES6 templates
      })
      document.getElementById('tbody').innerHTML=html_str  // se pone el html en su sitio

  })
  .catch(err=>console.log(err));
}

function detalle(i) {  // saca un modal con la información de cada coctel
  // saca un modal con receta[i]
  const receta=recetas[i-1];
  document.getElementById('detailModalLabel').textContent = receta.name;

  let html_str = ''
  receta.ingredients.forEach((ingredient)=>{
    html_str+= `<li>${ingredient.name}</li>`
  })
  document.getElementById('ingredientsList').innerHTML = html_str;

  html_str = ''
  receta.instructions.forEach((instruction)=>{
    html_str+= `<dd>- ${instruction}</dd>`
  })
  document.getElementById('instructionsList').innerHTML = html_str;
};

function showEditModal(i){
  const receta = recetas[i-1];
  document.getElementById('formModalLabel').textContent = 'Edit Recipe';
  document.getElementById('formName').value = receta.name;

  let html_str = ''
  receta.ingredients.forEach((ingredient, pos, arr)=>{
    html_str+= ingredient.name;
    if (pos!=arr.length-1)
      html_str+='\n'
  })
  document.getElementById('formIngredients').value = html_str;

  html_str = ''
  receta.instructions.forEach((instruction, pos, arr)=>{
    html_str+= instruction;
    if (pos!=arr.length-1)
      html_str+='\n'
  })
  document.getElementById('formInstructions').value = html_str;
  document.getElementById('btSaveForm').value = i;
}


function showDeleteModal(i){
  const receta = recetas[i-1];
  document.getElementById('deleteMessage').textContent = 'Do you want to delete '+receta.name+' ?';
  document.getElementById('btDelete').value=i;
}

function eliminar(i){
  const receta = recetas[i-1];
  fetch('/api/recipes/'+receta._id,{
    method: 'DELETE'
  })
  .then(()=>window.location.reload())
  .catch((err)=>alert(err));
}

document.getElementById('btDelete').addEventListener("click",event=>{
  eliminar(event.target.value);
});

document.getElementById('btAdd').addEventListener("click",function(){
  document.getElementById('recipeForm').reset();
  document.getElementById('formModalLabel').textContent = 'Add Recipe';
  document.getElementById('btSaveForm').value = 'add';
})

document.getElementById('btSaveForm').addEventListener("click",event=>{
  let method = event.target.value=='add' ? 'POST': 'PUT';
  let url = '/api/recipes';

  let body = {
    'name': document.getElementById('formName').value,
    'ingredients': document.getElementById('formIngredients').value.split('\n').map(ingredient=>{return {'name':ingredient};}),
    'instructions': document.getElementById('formInstructions').value.split('\n')
  };

  if (method=='PUT'){
    url+='/'+recetas[event.target.value-1]._id;
    body={'$set':body};
  }

  fetch(url,{
    method: method,
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(body)
  })
  .then(()=>window.location.reload())
  .catch((err)=>alert(err));
})

document.getElementById('formSearch').addEventListener("submit",event=>{
  event.preventDefault()
  let input = document.getElementById('inputSearch').value;
  let url='/api/recipes';

  if(input.trim().length !== 0)
    url='/recetas_de/'+input;
  
  document.getElementById('inputSearch').value="";
  fetchApp(url);
})

document.getElementById('btZoomIn').addEventListener("click", function(){
  let value = localStorage.getItem('fontSize');
  value++;

  localStorage.setItem('fontSize',value);
  document.getElementById('fontDiv').style.fontSize = value+'rem';
})


document.getElementById('btZoomOut').addEventListener("click", function(){
  let value = localStorage.getItem('fontSize');
  if(value>1)
    value--;

  localStorage.setItem('fontSize',value);
  document.getElementById('fontDiv').style.fontSize = value+'rem';
})

document.getElementById('btMode').addEventListener("click",function(){
  if (localStorage.getItem('mode')==='day')
    localStorage.setItem('mode','night');
  else
    localStorage.setItem('mode','day');

  changeMode();
})

function changeMode(){
  if (localStorage.getItem('mode')==='day'){
    document.getElementById('btMode').textContent = 'Modo noche';
    document.getElementById('modeLink').href = '';
  }
  else{
    document.getElementById('btMode').textContent = 'Modo dia';
    document.getElementById('modeLink').href = "static/css/dark.css";
  }

}