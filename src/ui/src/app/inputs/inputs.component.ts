import { Component, Input, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';

import { InputValueBase, TextValue } from './input-value-base';
import { InputValueService } from './input-value.service';
import { ScenarioService } from '../scenario.service';
import { Scenario } from '../scenario';

@Component({
  selector: 'app-inputs',
  templateUrl: './inputs.component.html',
  styleUrls: ['./inputs.component.css']
})
export class InputsComponent implements OnInit {
  scenario: Scenario;
  scenarioService: ScenarioService;
  inputValueService: InputValueService;

  @Input() input_values: InputValueBase<any>[] = [];
  form: FormGroup;

  constructor(scenarioService: ScenarioService, inputValueService: InputValueService) {
      this.scenarioService = scenarioService;
      this.inputValueService = inputValueService;
  }

  ngOnInit() {
      this.scenarioService.get_scenario().subscribe(
          scenario => {
              this.scenario = scenario;
              const input_values: InputValueBase<any>[] = [];
              for (const stage of this.scenario.stages) {
                  for (const input of stage.inputs) {
                      input_values.push(new TextValue({
                          key: input.id,
                          label: input.name,
                          value: 'default',
                          required: true,
                          order: 1
                      }));
                  }
              }
              this.input_values = input_values;
              this.form = this.inputValueService.toFormGroup(this.input_values);
          }
      );
  }

}
