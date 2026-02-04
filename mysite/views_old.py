import subprocess
from django.http import HttpResponse
from django.shortcuts import render
from .forms import GoogleSheetForm

# View to render the button page
def run_scripts_page(request):
    return render(request, 'run_scripts.html')

# Views to run specific scripts
def run_facebook_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Facebook V3.py"
    return execute_script(script_path)

def run_google_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Google V3.py"
    return execute_script(script_path)

def run_tiktok_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Tiktok V3.py"
    return execute_script(script_path)

def run_outbrain_script(request):
    script_path = "/home/Karmel/Karmel/Daily_reports/Google V3.py"
    return execute_script(script_path)

def run_newtabyes3_script(request):
    script_path = "/home/Karmel/Amit/newtabyes3.py"
    return execute_script(script_path)

def run_backupmaintonic_script(request):
    script_path = "/home/Karmel/Amit/backupmaintonic.py"
    return execute_script(script_path)

def run_obyesforreport_script(request):
    script_path = "/home/Karmel/Amit/obyesforreport 3.py"
    return execute_script(script_path)

def process_form_page(request):
    if request.method == 'POST':
        form = GoogleSheetForm(request.POST)
        if form.is_valid():
            # Get the form data
            sheet_id = form.cleaned_data['sheet_id']
            sheet_name = form.cleaned_data['sheet_name']
            import_number = form.cleaned_data['import_number']
            output_number = form.cleaned_data['output_number']
            model_name = form.cleaned_data['model_name']

            # Here we call your script and pass in the form values
            try:
                # You would pass these variables to your script
                result = run_gpt_executor(sheet_id, sheet_name, import_number, output_number, model_name)
                return render(request, 'result.html', {'result': result})  # Display the result after running the script
            except Exception as e:
                return render(request, 'process_form_page.html', {'form': form, 'error': str(e)})
    else:
        form = GoogleSheetForm()

    return render(request, 'process_form_page.html', {'form': form})

def run_gpt_executor(sheet_id, sheet_name, import_number, output_number, model_name):
    # This is where you will use subprocess to run the script with the input values
    # For now, I'll include an example subprocess call
    script_path = "/home/Karmel/Amit/GPT_executor.py"

    try:
        # Call the script using subprocess and pass in the arguments (from the form input)
        result = subprocess.run(
            ['python3', script_path, sheet_id, sheet_name, str(import_number), str(output_number), model_name],
            capture_output=True, text=True
        )
        return result.stdout  # Return the script output to be displayed
    except Exception as e:
        raise RuntimeError(f"Script failed to execute: {str(e)}")


# Helper function to execute scripts
def execute_script(script_path):
    try:
        # Run the script using subprocess
        result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        output = result.stdout

        return HttpResponse(f"Script executed successfully. Output: {output}")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
