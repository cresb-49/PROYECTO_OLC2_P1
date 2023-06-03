import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import * as ace from "ace-builds";

@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.css']
})
export class EditorComponent implements AfterViewInit {
  @ViewChild("editor") private editor!: ElementRef<HTMLInputElement>;
  @ViewChild("textbox") private textbox!: ElementRef<HTMLInputElement>;
  @ViewChild("contenedor") private contenedor!: ElementRef<HTMLElement>;


  codigoRef: string = '';
  mostrar: boolean = true;
  codeCRL: string = "";
  ubicacionEditor: string = "Linea: 1, Columna: 1";


  onKeyDownEvent(event: any) {
    if (event.key == 'Tab') {
      event.preventDefault();
      var start = this.textbox.nativeElement.selectionStart;
      var end = this.textbox.nativeElement.selectionEnd;
      // set textarea value to: text before caret + tab + text after caret
      if (start != null && end != null) {
        this.textbox.nativeElement.value = this.textbox.nativeElement.value.substring(0, start) +
          "\t" + this.textbox.nativeElement.value.substring(end);
        // put caret at right position again
        this.textbox.nativeElement.selectionStart = this.textbox.nativeElement.selectionEnd = start + 1;
      }
    }
  }

  mostrarUbicacion(linea: number, columna: number) {
    this.ubicacionEditor = "Linea: " + (linea + 1) + ", Columna: " + (columna + 1);
  }

  ngAfterViewInit(): void {
    ace.config.set("fontSize", "14px");
    ace.config.set('basePath', 'https://unpkg.com/ace-builds@1.4.12/src-noconflict');
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.setOption("useSoftTabs", false);
    aceEditor.setOption("tabSize", 4);
    aceEditor.setTheme('ace/theme/twilight');
    aceEditor.session.setMode('ace/mode/python');
    aceEditor.setValue(this.codeCRL);
    aceEditor.on("change", () => {
      this.codeCRL = aceEditor.getValue();
    });
    aceEditor.session.selection.on('changeCursor', () => {
      this.mostrarUbicacion(aceEditor.selection.getCursor().row, aceEditor.selection.getCursor().column)
    });
  }

  descargarCodigoEditor() {
    var blob = new Blob([this.codeCRL], { type: 'text/plain' });
    var url = window.URL.createObjectURL(blob);
    var anchor = document.createElement("a");
    anchor.download = this.codigoRef;
    anchor.href = url;
    anchor.click();
  }

  public getCodeCRL() {
    let temp = '';
    if (this.codeCRL.slice(-1) != '\n') {
      temp = this.codeCRL + "\n";
      this.codeCRL = temp;
    } else {
      temp = this.codeCRL;
    }
    return temp;
  }

  public visibilidad(estado: boolean) {
    if (estado) {
      this.contenedor.nativeElement.classList.remove('display-false');
    } else {
      this.contenedor.nativeElement.classList.add('display-false');
    }
  }

  public setCodeRef(nombre: string) {
    this.codigoRef = nombre;
  }

  public setCode(code: string) {
    this.codeCRL = code;
  }
}
