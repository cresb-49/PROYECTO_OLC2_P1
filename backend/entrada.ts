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

