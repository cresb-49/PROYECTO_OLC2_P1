import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  ViewChild,
} from '@angular/core';
import * as ace from 'ace-builds';
import { EditorComponent } from '../editor/editor.component';

@Component({
  selector: 'app-editor2',
  templateUrl: './editor2.component.html',
  styleUrls: ['./editor2.component.css']
})
export class Editor2Component implements AfterViewInit {
  @ViewChild('editor') private editor!: ElementRef<HTMLInputElement>;
  @ViewChild('textbox') private textbox!: ElementRef<HTMLInputElement>;
  @ViewChild('contenedor') private contenedor!: ElementRef<HTMLElement>;

  @Input() isEditable: boolean = true;
  @Input() nombreBoton: string = 'button';
  @Input() isLoadFile: boolean = false;

  @Input() resultConsole!: EditorComponent;
  nombreArchivo: string = 'C3D_GO';
  @Input() codigo: string = '';
  ubicacionEditor: string = 'Linea: 1, Columna: 1';

  copiarTextoText = 'Copiar Codigo';


  @Output() sendCodigo = new EventEmitter<string>();

  onKeyDownEvent(event: any) {
    if (event.key == 'Tab') {
      event.preventDefault();
      var start = this.textbox.nativeElement.selectionStart;
      var end = this.textbox.nativeElement.selectionEnd;
      // set textarea value to: text before caret + tab + text after caret
      if (start != null && end != null) {
        this.textbox.nativeElement.value =
          this.textbox.nativeElement.value.substring(0, start) +
          '\t' +
          this.textbox.nativeElement.value.substring(end);
        // put caret at right position again
        this.textbox.nativeElement.selectionStart =
          this.textbox.nativeElement.selectionEnd = start + 1;
      }
    }
  }

  mostrarUbicacion(linea: number, columna: number) {
    this.ubicacionEditor =
      'Linea: ' + (linea + 1) + ', Columna: ' + (columna + 1);
  }

  ngAfterViewInit(): void {
    ace.config.set('fontSize', '14px');
    ace.config.set(
      'basePath',
      'https://unpkg.com/ace-builds@1.4.12/src-noconflict'
    );
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.setOption('useSoftTabs', false);
    aceEditor.setOption('tabSize', 4);
    aceEditor.setTheme('ace/theme/twilight');
    aceEditor.session.setMode('ace/mode/golang');
    // Configurar el conjunto de caracteres
    //aceEditor.session.setMode('utf-8');
    aceEditor.setReadOnly(!this.isEditable);
    aceEditor.setValue(this.codigo);
    aceEditor.on('change', () => {
      this.codigo = aceEditor.getValue();
      this.sendCodigo.emit(this.codigo);
    });
    aceEditor.session.selection.on('changeCursor', () => {
      this.mostrarUbicacion(
        aceEditor.selection.getCursor().row,
        aceEditor.selection.getCursor().column
      );
    });
  }

  descargarCodigoEditor() {
    var blob = new Blob([this.codigo], { type: 'text/plain' });
    var url = window.URL.createObjectURL(blob);
    var anchor = document.createElement('a');
    if (this.isEditable) {
      anchor.download = this.nombreArchivo + '.go';
    } else {
      anchor.download = 'resultado_' + this.nombreArchivo + '.txt';
    }
    anchor.href = url;
    anchor.click();
  }

  public getCodeCRL() {
    let temp = '';
    if (this.codigo.slice(-1) != '\n') {
      temp = this.codigo + '\n';
      this.codigo = temp;
    } else {
      temp = this.codigo;
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

  public setNombreArchivo(nombre: string) {
    let split = nombre.split('.');
    this.nombreArchivo = split[0];
  }

  public setCode(code: string) {
    this.codigo = code;
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.setValue(this.codigo);
  }

  public copiarCodigo() {
    const aceEditor = ace.edit(this.editor.nativeElement);
    aceEditor.selectAll();
    var selectedText = aceEditor.getCopyText();
    let self = this;
    navigator.clipboard.writeText(selectedText).then(() => {
      self.copiarTextoText = 'Codigo Copiado!!!'
      setTimeout(() => {
        self.copiarTextoText = 'Copiar Codigo'
      }, 5000);
    }).catch((err) => {
      console.error("Error al copiar el texto: ", err)
    })
  }
  public cargarCodigo() {
    let input: HTMLInputElement = document.createElement('input');
    input.type = 'file';
    let self = this;
    input.onchange = (_) => {
      if (input.files) {
        let files = Array.from(input.files);
        self.handleFile(files);
        this.sendCodigo.emit(this.codigo);
      }
    };
    input.click();
  }
  public handleFile(fileList: any): void {
    let file = fileList[0];
    let fileReader: FileReader = new FileReader();
    let self = this;
    fileReader.onloadend = function (x) {
      let code: any = fileReader.result;
      self.setCode(code);
      self.setNombreArchivo(file.name);
    };
    fileReader.readAsText(file);
  }
}
