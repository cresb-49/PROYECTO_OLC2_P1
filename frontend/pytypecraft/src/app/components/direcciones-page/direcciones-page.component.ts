import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { EditorComponent } from '../editor/editor.component';
import { CompileService } from 'src/app/servicios/compile.service';

@Component({
  selector: 'app-direcciones-page',
  templateUrl: './direcciones-page.component.html',
  styleUrls: ['./direcciones-page.component.css'],
})
export class DireccionesPageComponent implements AfterViewInit {
  displayedColumns: string[] = [
    'tipo',
    'descripcion',
    'linea',
    'columna',
    'fechaHora',
  ];

  dataSource = [];

  public codigo = '';
  @ViewChild('consoleCode') codeConsole!: EditorComponent;
  @ViewChild('consoleResult') resultConsole!: EditorComponent;

  constructor(private compileService: CompileService) {}

  /**
   * Al iniciar la vista de codigo debemos comprovar si hay un codigo guardado en las cookies
   * para iniciar con codigo precargado
   */
  ngAfterViewInit(): void {
    this.refreshPage();
  }

  private refreshPage(): void {
    if (localStorage.getItem('c3d') != null) {
      this.setConsola();
      this.setTablaErrores();
    }
  }

  public setConsola(): void {
    //borramos el contenido de la consola
    let code = localStorage.getItem('code_c3d')!;
    this.codeConsole.setCode(code);

    //borramos el contenido de la consola
    let consola = '';

    let errores = JSON.parse(localStorage.getItem('c3d')!).errores;

    if (errores.length > 0) {
      consola = 'SE ENCONTRARON ERRORES, PARA MAS DETALLE VER LA TABLA\n';
      errores.forEach((element: any) => {
        consola +=
          '\n----ERROR----\n\nTipo de error: ' +
          element.tipo +
          '\nMotivo de error: ' +
          element.descripcion +
          '\n';
      });
    } else {
      //borramos el contenido de la consola
      consola = JSON.parse(localStorage.getItem('c3d')!).c3d;
    }

    this.resultConsole.setCode(consola);
  }

  public sendCode(): void {
    //Envia el codigo escrito en la consola hacia el backend
    this.compileService.sendCodeFase2(this.codigo).subscribe((r) => {
      console.log(r);
      localStorage.removeItem('code_c3d');
      localStorage.removeItem('c3d');
      localStorage.setItem('c3d', JSON.stringify(r));
      localStorage.setItem('code_c3d', this.codigo);
      this.refreshPage(); //mandamos ha refrescar la pagina
    });
  }

  /**
   * Este metodo se activa cada vez que el usuairo hace un tecleo en la consola habiitada
   * @param codigo codigo que escribe el usuario
   */
  public setCodigo(codigo: string): void {
    //eteamos el codigo local con el escrito por el usuario
    this.codigo = codigo;
  }

  private setTablaErrores(): void {
    let errores = JSON.parse(localStorage.getItem('c3d')!).errores;
    this.dataSource = errores;
  }
}
