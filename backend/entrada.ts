//Pruebas del print con expreciones artimeticas
let v: any;
v = 5;
//Pruebas de array
let numeros:any[] = [1, 2, 3, 4, [5,6]];
let nume = [1, 2, 3, 4, [5,6]];
console.log(v + 5);
console.log([2,5,6][2]-1+v);
console.log(numeros[4][1]);
console.log(nume[4][1]);
//console.log(5[0]);
let palabras: string[] = ["Hola", "Mundo", "en", "TypeScript"];
let booleanos: boolean[] = [true, false, true];
let anys: any[] = ["Hola", false, 3];

console.log(palabras[0]);
console.log(booleanos[0]);
console.log(anys[0]);

for (let index = 0; index < 12 ; index++) {
    console.log(index);
}

let str = "5";
for (let iterator of str) {
  console.log(iterator);
}

for (let iterator of "hola") {
    console.log(iterator);
}

for (let iterator of [1,3,4]) {
    console.log(iterator);
}

let cont = 0;
while (cont < 3) {
   cont = cont + 1;
    console.log(cont);
}

let var4 = 'global';

function nombre(hola:string) {
  let nose:string =  hola;
  console.log(nose.toUpperCase());
  console.log(var4);
}

nombre("hola");

let str2= 5;
console.log(str2);


let variable = "hola como esta mi amor linda jahahahah que hace?";

let var2 = variable.split(" ");

console.log(var2);

let var3 = 2.33456;

console.log(var3.toFixed(2));


let var4 = 223234234.33456;

console.log(var3.toExponential(5));
