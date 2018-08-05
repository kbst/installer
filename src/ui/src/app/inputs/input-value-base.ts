export class InputValueBase<T> {
  id: number;
  stage_id: number;
  type: string;
  name: string;
  value: T;
  label: string;
  min: number;
  max: number;
  step: number;
  required: boolean;
  order: number;
  controlType: string;

  constructor(options: {
      id?: number,
      stage_id?: number,
      type?: string;
      name?: string,
      value?: T,
      label?: string,
      min?: number,
      max?: number,
      step?: number,
      required?: boolean,
      order?: number,
      controlType?: string
    } = {}) {
    this.id = options.id;
    this.stage_id = options.stage_id;
    this.type = options.type;
    this.name = options.name;
    this.value = options.value;
    this.label = options.label || '';
    this.min = options.min || null;
    this.max = options.max || null;
    this.step = options.step || null;
    this.required = !!options.required;
    this.order = options.order === undefined ? this.id : options.order;
    this.controlType = options.controlType || '';
  }
}

export class TextValue extends InputValueBase<string> {
  controlType = 'textbox';
  type: string;

  constructor(options: {} = {}) {
    super(options);
    this.type = options['type'] || '';
  }
}
