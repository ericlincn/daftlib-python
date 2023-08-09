class Js:

    # Usage:
    # Flask blueprint:
    # return Js.redirect(url_for("auth.login_view"))
    @staticmethod
    def redirect(target:str) -> str:
        return "<script>window.location.href='" + target + "'</script>"
    
    # Usage:
    # Jinja2 + htmx template:
    # {{ htmx_script | safe }}
    # 
    # <input type="email" id="email" name="email" required
    #        hx-get="/auth/captcha/email"
    #        htmx:beforeOnLoad: before_on_load(event)">
    # 
    # Flask blueprint:
    # if request.method == 'GET':
    #    return render_template("register.html", htmx_script = Js.htmx_ignore_error([422, 429]))
    @staticmethod
    def htmx_ignore_error(code_list:list) -> str:
        for i in range(0, len(code_list)):
            code_list[i] = "event.detail.xhr.status === " + str(code_list[i])
        statement:str = " | ".join(code_list)

        return """<script>
            function before_on_load(event) { 
                if ("""+ statement +""") { 
                    event.detail.shouldSwap = true;
                    event.detail.isError = false;
                }
            }
        </script>"""
    