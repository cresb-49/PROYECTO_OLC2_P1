import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { EditorComponent } from '../editor/editor.component';

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
  /**
   * Al iniciar la vista de codigo debemos comprovar si hay un codigo guardado en las cookies
   * para iniciar con codigo precargado
   */
  ngAfterViewInit(): void {
    this.refreshPage();
  }

  private refreshPage(): void {
    if (localStorage.getItem('compile') != null) {
      this.setConsola();
    }
  }

  public setConsola(): void {
    //borramos el contenido de la consola
    let consola = '';
    let c3d = JSON.parse(localStorage.getItem('compile')!).c3d;
    consola = c3d;
    this.resultConsole.setCode(consola);
  }

  public sendCode(): void {
    //Envia el codigo escrito en la consola hacia el backend
    // this.compileService.sendCode(this.codigo).subscribe((r) => {
    //   console.log(r);
    //   localStorage.removeItem('compile');
    //   localStorage.removeItem('code');
    //   localStorage.setItem('compile', JSON.stringify(r));
    //   localStorage.setItem('code', this.codigo);
    //   this.refreshPage(); //mandamos ha refrescar la pagina
    // });
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
    let errores = JSON.parse(localStorage.getItem('compile')!).errores;
    this.dataSource = errores;
  }
}
