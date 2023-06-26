interface Persona {
    nombre: string;
    edad: number;
}

let persona = [{nombre:'Juan',edad:23},{nombre:'Alberto',edad:30}];

let valor = persona[0];
console.log(valor.nombre);
console.log(valor.edad);
valor = persona[1];
console.log(valor.nombre);
console.log(valor.edad);