export enum Status {
    PENDING = 0,
    SUCCESS = 1,
    ERROR = 2,
    SKIPPED = 3
}

export class Input {
    public id: number;
    public stage_id: number;
    public name: string;
    public value: string;

    constructor(obj: any) {
        this.id = obj.id;
        this.stage_id = obj.stage_id;
        this.name = obj.name;
        this.value = obj.value;
    }
}

export class Step {
    public id: number;
    public stage_id: number;
    public name: string;
    public result: any;
    public status: Status;

    constructor(obj: any) {
        this.id = obj.id;
        this.stage_id = obj.stage_id;
        this.name = obj.name;
        this.result = obj.result;
        const enumVal: Status = (<any>Status)[obj.status.name];
        this.status = enumVal;
    }
}

export class Stage {
    public id: number;
    public name: string;
    public description: string;
    public inputs: Input[] = [];
    public steps: Step[] = [];
    public status: Status;

    constructor(obj: any) {
        this.id = obj.id;
        this.name = obj.name;
        this.description = obj.description;

        for (const input of obj.inputs) {
             this.inputs.push(new Input(input));
        }

        for (const step of obj.steps) {
             this.steps.push(new Step(step));
        }

        const enumVal: Status = (<any>Status)[obj.status.name];
        this.status = enumVal;
    }
}

export class Scenario {
    public stages: Stage[] = [];
    public status: Status;

    constructor(obj: any) {
        for (const stage of obj.stages) {
             this.stages.push(new Stage(stage));
        }
        const enumVal: Status = (<any>Status)[obj.status.name];
        this.status = enumVal;
    }
}
