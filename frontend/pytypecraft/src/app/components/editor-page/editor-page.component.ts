import { Component, OnInit,AfterViewInit, ViewChild } from '@angular/core';
import { EditorComponent } from '../editor/editor.component';
import { CompileService } from 'src/app/servicios/compile.service';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-editor-page',
  templateUrl: './editor-page.component.html',
  styleUrls: ['./editor-page.component.css'],
})
export class EditorPageComponent implements AfterViewInit {
  @ViewChild('consoleResult') resultConsole!: EditorComponent;

  @ViewChild('consoleCode') codeConsole!: EditorComponent;

  displayedColumns: string[] = [
    'tipo',
    'descripcion',
    'linea',
    'columna',
    'fechaHora',
  ];

  dataSource = [];

  public codigo = '';

  constructor(
    private compileService: CompileService,
    private cookieService: CookieService
  ) {}


  /**
   * Al iniciar la vista de codigo debemos comprovar si hay un codigo guardado en las cookies
   * para iniciar con codigo precargado
   */
  ngAfterViewInit(): void {
     //si la cookie de codigo existe entonces debemos cargar el codigo en la consola
     if (this.cookieService.check('code')) {
      this.codigo = this.cookieService.get('code');
      this.codeConsole.setCode(this.codigo);
    }

    if (this.cookieService.check('compile')) {
      this.setConsola();
      this.setTablaErrores();
    }
  }

  public setConsola(): void {
    //borramos el contenido de la consola
    let consola = "";

    let nuevaSalida = JSON.parse(this.cookieService.get('compile')).consola;

    nuevaSalida.forEach((element: any) => {
      consola += element + '\n';
    });

    this.resultConsole.setCode(consola)
  }

  public sendCode(): void {
    //Envia el codigo escrito en la consola hacia el backend
    this.compileService.sendCode(this.codigo).subscribe((r) => {
      console.log(r);
      this.cookieService.delete('compile');
      this.cookieService.delete('code');
      this.cookieService.set('compile', JSON.stringify(r));
      this.cookieService.set('code', this.codigo);
      this.setConsola();
      this.setTablaErrores();
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

  private setTablaErrores():void{
    let errores = JSON.parse(this.cookieService.get('compile')).errores;
    this.dataSource = errores;
  }
}
