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
              for (const stage of this.scenario.stages) {
                  for (const input of stage.inputs) {
                      // Check if we already have a form field for that input
                      const i = this.input_values.findIndex(
                          _input_value => _input_value.name === input.name
                      );

                      // Update existing or add new accordingly
                      if (i > -1) {
                          const input_value = this.input_values[i];
                          input_value.id = input.id;
                          input_value.stage_id = input.stage_id;
                          input_value.type = input.type;
                          input_value.name = input.name;
                          input_value.value = input.value;
                          input_value.label = input.label;
                          input_value.min = input.min;
                          input_value.max = input.max;
                          input_value.step = input.step;
                          input_value.required = true;
                          input_value.order = 1;
                      } else {
                          this.input_values.push(new TextValue({
                              id: input.id,
                              stage_id: input.stage_id,
                              type: input.type,
                              name: input.name,
                              value: input.value,
                              label: input.label,
                              min: input.min,
                              max: input.max,
                              step: input.step,
                              required: true,
                              order: 1
                          }));
                      }
                  }
              }
              this.form = this.inputValueService.toFormGroup(this.input_values);
          }
      );
  }

  update_inputs(input_value: InputValueBase<string>, form: FormGroup) {
    const input = this.scenario.stages[input_value.stage_id].inputs[input_value.id];
    input.value = form.value[input_value.label];
    this.scenarioService.update_inputs(this.scenario);
  }

}
