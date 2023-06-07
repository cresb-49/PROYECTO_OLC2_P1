//Ejemplo 1: Entornos. Variables globales y locales
let x: number = (3 * 5);//15
let str = "Saludo";
let str2 = 'Saludo';

function ejemplos() {
    str = "Ejemplo";
    let x = 0;
    for (let i = 0; i < 10; i++) {
        let y: number; //Creacion de una variable local
        y = i * 2;
        console.log(x);
    }
    console.log(x);//0 --> La variable nunca fue modificada
}

function ejemplo2() {
    let z = 0;
}

ejemplos();
console.log(x); //15
console.log(str);//Ejemplo --> Modificada dentro de ejemplo()

