/* ---- HEADER ----- */
package main;

import(
	"fmt"
	"math"
)
var t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,t32,t33,t34,t35,t36,t37,t38,t39,t40,t41,t42,t43,t44,t45,t46,t47,t48,t49,t50,t51,t52,t53,t54,t55,t56,t57,t58,t59,t60,t61,t62,t63,t64,t65,t66,t67,t68,t69,t70,t71,t72,t73,t74,t75,t76,t77,t78,t79,t80,t81,t82,t83,t84,t85,t86,t87,t88,t89,t90,t91,t92,t93,t94,t95,t96,t97 float64;

var P, H float64;
var stack[30101999] float64;
var heap[30101999] float64;

/* --- NATIVAS --- */
	func printString(){
	t1 = P + 1;
	t2 = stack[int(t1)];
	L1:
		t3 = heap[int(t2)];
		if t3 == -1 {goto L0;}
		fmt.Printf("%c", int(t3));
		t2 = t2 + 1;
		goto L1;
	L0:
	}

func main(){
	/* ** compilacion de variable val1 ** */
	stack[int(0)] = 1;
	/* ** fin de compilacion variable val1 ** */
	/* ** compilacion de variable val2 ** */
	stack[int(1)] = 10;
	/* ** fin de compilacion variable val2 ** */
	/* ** compilacion de variable val3 ** */
	stack[int(2)] = 2021.202;
	/* ** fin de compilacion variable val3 ** */
	t0 = H;
	heap[int(H)] = 80;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 98;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 108;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 118;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 98;
	H = H + 1;
	heap[int(H)] = 108;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 10;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t4 = P + 3;
	t4 = t4 + 1;
	stack[int(t4)] = t0;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t5 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	/* ** compilacion de acceso de variable val1 ** */
	t6 = stack[int(0)];
	/* ** fin compilacion de acceso de variable val1 ** */
	fmt.Printf("%f", t6);
	t7 = H;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t8 = P + 3;
	t8 = t8 + 1;
	stack[int(t8)] = t7;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t9 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	/* ** compilacion de acceso de variable val2 ** */
	t10 = stack[int(1)];
	/* ** fin compilacion de acceso de variable val2 ** */
	fmt.Printf("%f", t10);
	t11 = H;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t12 = P + 3;
	t12 = t12 + 1;
	stack[int(t12)] = t11;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t13 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	/* ** compilacion de acceso de variable val3 ** */
	t14 = stack[int(2)];
	/* ** fin compilacion de acceso de variable val3 ** */
	fmt.Printf("%f", t14);
	fmt.Println("")
	t15 = H;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t16 = P + 3;
	t16 = t16 + 1;
	stack[int(t16)] = t15;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t17 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	/* ** compilacion de acceso de variable val1 ** */
	t18 = stack[int(0)];
	/* ** fin compilacion de acceso de variable val1 ** */
	t19 = t18 + 41;
	t20 = 123 * 4;
	t21 = 2 * 2;
	t22 = 2 + t21;
	t23 = t20 / t22;
	t24 = t19 - t23;
	t25 =  float64(int(125) % int(5));
	t26 = 10 + t25;
	t27 =  math.Pow(2, 2);
	t28 = t26 * t27;
	t29 = t24 - t28;
	/* ** compilacion de asignacion de variable val1 ** */
	stack[int(0)] = t29;
	/* ** fin de compilacion de asignacion variable val1 ** */
	t30 = -1 * 10;
	t31 = 12 + t30;
	t32 =  float64(int(11) % int(t31));
	t33 = 11 * t32;
	t34 = 22 / 2;
	t35 = t33 + t34;
	/* ** compilacion de asignacion de variable val2 ** */
	stack[int(1)] = t35;
	/* ** fin de compilacion de asignacion variable val2 ** */
	t36 =  math.Pow(12, 2);
	t37 = 5 * t36;
	t38 =  math.Pow(2, t37);
	t39 = 25 / 5;
	t40 = t38 + t39;
	/* ** compilacion de asignacion de variable val3 ** */
	stack[int(2)] = t40;
	/* ** fin de compilacion de asignacion variable val3 ** */
	t41 = H;
	heap[int(H)] = 80;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 98;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 103;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 195;
	H = H + 1;
	heap[int(H)] = 179;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 118;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 98;
	H = H + 1;
	heap[int(H)] = 108;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 121;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 116;
	H = H + 1;
	heap[int(H)] = 109;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 116;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t42 = P + 3;
	t42 = t42 + 1;
	stack[int(t42)] = t41;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t43 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	/* ** compilacion de acceso de variable val1 ** */
	t44 = stack[int(0)];
	/* ** fin compilacion de acceso de variable val1 ** */
	fmt.Printf("%f", t44);
	t45 = H;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t46 = P + 3;
	t46 = t46 + 1;
	stack[int(t46)] = t45;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t47 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	/* ** compilacion de acceso de variable val2 ** */
	t48 = stack[int(1)];
	/* ** fin compilacion de acceso de variable val2 ** */
	fmt.Printf("%f", t48);
	t49 = H;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t50 = P + 3;
	t50 = t50 + 1;
	stack[int(t50)] = t49;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t51 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	/* ** compilacion de acceso de variable val3 ** */
	t52 = stack[int(2)];
	/* ** fin compilacion de acceso de variable val3 ** */
	fmt.Printf("%f", t52);
	fmt.Println("")
	t53 = H;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t54 = P + 3;
	t54 = t54 + 1;
	stack[int(t54)] = t53;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t55 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	t56 = H;
	heap[int(H)] = 79;
	H = H + 1;
	heap[int(H)] = 80;
	H = H + 1;
	heap[int(H)] = 69;
	H = H + 1;
	heap[int(H)] = 82;
	H = H + 1;
	heap[int(H)] = 65;
	H = H + 1;
	heap[int(H)] = 67;
	H = H + 1;
	heap[int(H)] = 73;
	H = H + 1;
	heap[int(H)] = 79;
	H = H + 1;
	heap[int(H)] = 78;
	H = H + 1;
	heap[int(H)] = 69;
	H = H + 1;
	heap[int(H)] = 83;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t57 = P + 3;
	t57 = t57 + 1;
	stack[int(t57)] = t56;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t58 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	t59 = H;
	heap[int(H)] = 67;
	H = H + 1;
	heap[int(H)] = 79;
	H = H + 1;
	heap[int(H)] = 78;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t60 = P + 3;
	t60 = t60 + 1;
	stack[int(t60)] = t59;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t61 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	t62 = H;
	heap[int(H)] = 67;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t63 = P + 3;
	t63 = t63 + 1;
	stack[int(t63)] = t62;
	/* --- NUEVO ENTORNO --- */
	P = P + 3;
	printString();
	t64 = stack[int(P)];
	P = P - 3;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	t65 = H;
	heap[int(H)] = 65;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 109;
	H = H + 1;
	heap[int(H)] = 117;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 58;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	/* ** compilacion de variable despedida ** */
	stack[int(3)] = t65;
	/* ** fin de compilacion variable despedida ** */
	t66 = H;
	heap[int(H)] = 72;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 108;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 77;
	H = H + 1;
	heap[int(H)] = 117;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 33;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	/* ** compilacion de variable saludo ** */
	stack[int(4)] = t66;
	/* ** fin de compilacion variable saludo ** */
	/* ** compilacion de acceso de variable saludo ** */
	t67 = stack[int(4)];
	/* ** fin compilacion de acceso de variable saludo ** */
	t68 = P + 5;
	t68 = t68 + 1;
	stack[int(t68)] = t67;
	/* --- NUEVO ENTORNO --- */
	P = P + 5;
	printString();
	t69 = stack[int(P)];
	P = P - 5;
	/* --- RETORNO DE ENTORNO --- */
	/* ** compilacion de acceso de variable despedida ** */
	t70 = stack[int(3)];
	/* ** fin compilacion de acceso de variable despedida ** */
	t71 = P + 5;
	t71 = t71 + 1;
	stack[int(t71)] = t70;
	/* --- NUEVO ENTORNO --- */
	P = P + 5;
	printString();
	t72 = stack[int(P)];
	P = P - 5;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	t73 = H;
	heap[int(H)] = 80;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 98;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 108;
	H = H + 1;
	heap[int(H)] = 103;
	H = H + 1;
	heap[int(H)] = 117;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 102;
	H = H + 1;
	heap[int(H)] = 117;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 116;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 118;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 80;
	H = H + 1;
	heap[int(H)] = 121;
	H = H + 1;
	heap[int(H)] = 84;
	H = H + 1;
	heap[int(H)] = 121;
	H = H + 1;
	heap[int(H)] = 112;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 67;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 102;
	H = H + 1;
	heap[int(H)] = 116;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t74 = P + 5;
	t74 = t74 + 1;
	stack[int(t74)] = t73;
	/* --- NUEVO ENTORNO --- */
	P = P + 5;
	printString();
	t75 = stack[int(P)];
	P = P - 5;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	t76 = H;
	heap[int(H)] = 70;
	H = H + 1;
	heap[int(H)] = 117;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 108;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 100;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = 99;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 118;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 114;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = 105;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 110;
	H = H + 1;
	heap[int(H)] = 101;
	H = H + 1;
	heap[int(H)] = 115;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t77 = P + 5;
	t77 = t77 + 1;
	stack[int(t77)] = t76;
	/* --- NUEVO ENTORNO --- */
	P = P + 5;
	printString();
	t78 = stack[int(P)];
	P = P - 5;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	/* ** compilacion de variable aprox_1 ** */
	stack[int(5)] = 3.141516;
	/* ** fin de compilacion variable aprox_1 ** */
	/* ** compilacion de acceso de variable aprox_1 ** */
	t79 = stack[int(5)];
	/* ** fin compilacion de acceso de variable aprox_1 ** */
	fmt.Printf("%f", t79);
	/* ** compilacion de acceso de variable aprox_1 ** */
	t80 = stack[int(5)];
	/* ** fin compilacion de acceso de variable aprox_1 ** */
	fmt.Printf("%f", t80);
	fmt.Println("")
	t81 = H;
	heap[int(H)] = 50;
	H = H + 1;
	heap[int(H)] = 48;
	H = H + 1;
	heap[int(H)] = 49;
	H = H + 1;
	heap[int(H)] = 57;
	H = H + 1;
	heap[int(H)] = 48;
	H = H + 1;
	heap[int(H)] = 51;
	H = H + 1;
	heap[int(H)] = 56;
	H = H + 1;
	heap[int(H)] = 54;
	H = H + 1;
	heap[int(H)] = 53;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	/* ** compilacion de variable carnet ** */
	stack[int(6)] = t81;
	/* ** fin de compilacion variable carnet ** */
	t82 = H;
	heap[int(H)] = 72;
	H = H + 1;
	heap[int(H)] = 111;
	H = H + 1;
	heap[int(H)] = 108;
	H = H + 1;
	heap[int(H)] = 97;
	H = H + 1;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t83 = P + 7;
	t83 = t83 + 1;
	stack[int(t83)] = t82;
	/* --- NUEVO ENTORNO --- */
	P = P + 7;
	printString();
	t84 = stack[int(P)];
	P = P - 7;
	/* --- RETORNO DE ENTORNO --- */
	/* ** compilacion de acceso de variable carnet ** */
	t85 = stack[int(6)];
	/* ** fin compilacion de acceso de variable carnet ** */
	t86 = P + 7;
	t86 = t86 + 1;
	stack[int(t86)] = t85;
	/* --- NUEVO ENTORNO --- */
	P = P + 7;
	printString();
	t87 = stack[int(P)];
	P = P - 7;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	/* ** compilacion de acceso de variable val1 ** */
	t88 = stack[int(0)];
	/* ** fin compilacion de acceso de variable val1 ** */
	fmt.Printf("%f", t88);
	t89 = H;
	heap[int(H)] = 32;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t90 = P + 7;
	t90 = t90 + 1;
	stack[int(t90)] = t89;
	/* --- NUEVO ENTORNO --- */
	P = P + 7;
	printString();
	t91 = stack[int(P)];
	P = P - 7;
	/* --- RETORNO DE ENTORNO --- */
	/* ** compilacion de acceso de variable carnet ** */
	t92 = stack[int(6)];
	/* ** fin compilacion de acceso de variable carnet ** */
	t93 = P + 7;
	t93 = t93 + 1;
	stack[int(t93)] = t92;
	/* --- NUEVO ENTORNO --- */
	P = P + 7;
	printString();
	t94 = stack[int(P)];
	P = P - 7;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")
	t95 = H;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = 45;
	H = H + 1;
	heap[int(H)] = -1;
	H = H + 1;
	t96 = P + 7;
	t96 = t96 + 1;
	stack[int(t96)] = t95;
	/* --- NUEVO ENTORNO --- */
	P = P + 7;
	printString();
	t97 = stack[int(P)];
	P = P - 7;
	/* --- RETORNO DE ENTORNO --- */
	fmt.Println("")

}