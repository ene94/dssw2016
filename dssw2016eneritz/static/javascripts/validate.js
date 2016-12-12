jQuery(function ($) {
  $("#formulario").validate({
    rules: {
      username: "required",
      password: "required",
      password2: {
        equalTo: '#password'
      },
      email: {
        required: true,
        email: true
      }
    },

    messages: {
      username: "  introduce usuario",
      password: "  introduce contraseña",
      password2: {
        required: "  introduce contraseña",
        equalTo: "  las contraseñas deben ser iguales"
      },
      email: "  introduce email"
    }
  });
});
