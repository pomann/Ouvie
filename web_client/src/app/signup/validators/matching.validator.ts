import { FormGroup } from '@angular/forms';


export function matching(matchOne: string, matchTwo: string) {
    return (formGroup: FormGroup) => {
        const varOne = formGroup.controls[matchOne];
        const varTwo = formGroup.controls[matchTwo];

        if (varOne.errors && !varTwo.errors.mustMatch) {
            return;
        }

        if (varOne.value !== varTwo.value) {
            varTwo.setErrors({ mustMatch: true });
            console.log('AyyWhore');
        } else {
            varTwo.setErrors(null);
            console.log('Thruee');
        }
    };
}
