import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { EditorComponent } from '../editor/editor.component';

@Component({
  selector: 'app-direcciones-page',
  templateUrl: './direcciones-page.component.html',
  styleUrls: ['./direcciones-page.component.css'],
})
export class DireccionesPageComponent implements AfterViewInit {
  public codigo = '';
  @ViewChild('consoleCode') codeConsole!: EditorComponent;
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
    this.codeConsole.setCode(consola);
  }
}
