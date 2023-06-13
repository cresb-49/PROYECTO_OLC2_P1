interface Carro {
    placa: string;
    color: string;
    tipo: string;
};

let c1: Carro = {
    placa: "090PLO",
    color: 'gris',
    tipo: 'mecanico'
};

let c2: Carro = {
    placa: "POS921",
    color: 'verde',
    tipo: 'automatico'
};

//Asignacion de atributos
c1.color = 'cafe';
c2.color = 'rojo';

//Acceso Atributo
console.log(c1.color);

console.log(String(Number("35")), "No se jajaj");

console.log([1,2,3,[4,5,[6,[6,[6,[6,7,[6,7,5]],5],5],7,8]]]); // Esta funcion sera extra, la veremos en clase para que la implementen

