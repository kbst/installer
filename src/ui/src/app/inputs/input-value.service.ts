import { Injectable } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { InputValueBase } from './input-value-base';

@Injectable()
export class InputValueService {
  constructor() { }

  toFormGroup(inputs: InputValueBase<any>[] ) {
    const group: any = {};

    inputs.forEach(input => {
      group[input.key] = input.required ? new FormControl(input.value || '', Validators.required)
                                        : new FormControl(input.value || '');
    });
    return new FormGroup(group);
  }
}
