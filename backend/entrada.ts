//Ejemplo 1: Entornos. Variables globales y locales
let x: number = (3 * 5);//15
let str = "Saludo";

function ejemplos() {
    str = "Ejemplo";
    let x = 0;
    for (let i = 0; i < 10; i++) {
        let x: number; //Creacion de una variable local
        x = i * 2;
        console.log(x);
    }
    console.log(x);//0 --> La variable nunca fue modificada
}

ejemplos();
console.log(x); //15
console.log(str);//Ejemplo --> Modificada dentro de ejemplo()

