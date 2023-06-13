import { Component, ViewChild } from '@angular/core';
import { EditorComponent } from '../editor/editor.component';
import { CompileService } from 'src/app/servicios/compile.service';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-editor-page',
  templateUrl: './editor-page.component.html',
  styleUrls: ['./editor-page.component.css'],
})
export class EditorPageComponent {
  @ViewChild('consoleResult') resultConsole!: EditorComponent;

  public codigo = '';
  constructor(
    private compileService: CompileService,
    private cookieService: CookieService
  ) {}

  public sendCode() {
    //Envia el codigo escrito en la consola hacia el backend
    this.compileService.sendCode(this.codigo).subscribe((r) => {
      console.log(r);

      this.cookieService.delete('compile');
      this.cookieService.delete('code');
      this.cookieService.set('compile', r);
      this.cookieService.set('code', this.codigo);
    });
  }

  /**
   * Este metodo se activa cada vez que el usuairo hace un tecleo en la consola habiitada
   * @param codigo codigo que escribe el usuario
   */
  public setCodigo(codigo: string) {
    //eteamos el codigo local con el escrito por el usuario
    this.codigo = codigo;
  }
}
