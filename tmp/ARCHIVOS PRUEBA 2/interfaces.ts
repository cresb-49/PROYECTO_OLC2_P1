interface Actor {
    nombre: string;
    edad: number;
}

interface Pelicula {
    nombre: string;
    posicion: number;
}



let actores = ["Elizabeth Olsen", "Adam Sandler", "Christian Bale", "Jennifer Aniston"];
let peliculas = ["Avengers: Age of Ultron", "Mr. Deeds", "Batman: The Dark Knight", "Marley & Me"];


function crearActor(nombre: string, edad: number): Actor {
    return {nombre: nombre, edad: edad};
}

function crearPelicula(nombre: string, posicion: number): Pelicula {
    return { nombre: nombre, posicion: posicion };
}
function imprimir(actor:any) {
	console.log(actor.nombre);
}
function contratos() {
    for (let i = 1; i < 3; i++) {
        if (i < 4) {
            let actor = crearActor(actores[i - 1], i + 38);
            let pelicula = crearPelicula(peliculas[i - 1], i);
           
            imprimir(actor);
        }
        
    }
}

contratos();