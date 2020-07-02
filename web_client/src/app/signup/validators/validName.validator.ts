import { FormGroup } from '@angular/forms';


export function validName(matchOne: string) {
    return (formGroup: FormGroup) => {
        const varOne = formGroup.controls[matchOne];

        if (varOne.errors) {
            return;
        }

        if (!varOne.value.match(/^[a-z][a-z ,.'-]+$/i)) {
            varOne.setErrors({ valid: true });
        } else {
            varOne.setErrors(null);
        }
    };
}
