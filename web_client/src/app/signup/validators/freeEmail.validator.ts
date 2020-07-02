import { FormGroup } from '@angular/forms';


export function freeEmail(matchOne: string) {
    return (formGroup: FormGroup) => {
        const varOne = formGroup.controls[matchOne];

        // if (varOne.value) {
        //     varOne.setErrors({ free: true });
        //     console.log('AyyWhore');
        // } else {
        //     varOne.setErrors(null);
        //     console.log('Thruee');
        // }
    };
}
