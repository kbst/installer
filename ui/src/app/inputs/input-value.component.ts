import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

import { InputValueBase } from './input-value-base';

@Component({
  selector: 'app-input-value',
  templateUrl: './input-value.component.html',
  styleUrls: ['./input-value.component.css']
})
export class InputValueComponent {
  @Input() input_value: InputValueBase<any>;
  @Input() form: FormGroup;
  get isValid() { return this.form.controls[this.input_value.label].valid; }
}
