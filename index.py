'''
	Index page. Present the user with a "start" button that starts up the
	fruit machine
'''

def index(req):
	output = page_head()
	args = parse_args(req.args)
	if args['action'] == 'start':
		output += page_start(args)
	else:
		output += page_index()
	output += page_foot()
	return output

'''
Given a request URL string, parse the args into a dictionary and return it.
This does not attempt to deal intelligently with repeated args.
'''
def parse_args(arg_string):
	arg_list = arg_string.split("&")
	arg_dict = {}
	for arg_pair in arg_list:
		arg_tuple = arg_pair.split("=")
		arg_dict[arg_tuple[0]] = arg_tuple[1]
	return arg_dict

def page_index():
	return '''
		<form action="index.py">
			<div class="form-group">
				<input type="hidden" name="action" value="start"/>
				<label>
					Please enter your name
					<input type="text" name="name" class="form-control"/>
				</label>
			</div>
			<div class="col-12">
				<button type="submit" class="btn btn-primary">Start</button>
			</div>
		</form>
	'''

def page_start(args):
	output = ''
	if args.get('name', False):
		output += '''
		<form action="index.py">
		<div class="row">
			<div class="col-12 form-group">
				<input type="hidden" name="action" value="start"/>
				<input type="hidden" name="name" value="''' + args.get('name') + '''"/>
				<label>
					On a scale from zero to eleven, how gay are you?
				</label>
			</div>
		'''
		for gay in range(12):
			output += '''
			<div class="col-1">
				<input type="submit" class="btn btn-primary" name="gay" value="'''
			output += gay.__str__()
			output += '''"/>
			</div>
			'''
		output += '''
		</div>
		</form>
	'''
	else:
		output += '''
		<div class="alert alert-warning" role="alert">
			Please enter a name
		</div>
		'''
		output += page_index()
	return output

def page_head():
	return '''
<!DOCTYPE html>
<html lang="en">
<head>
	<!-- Required meta tags -->
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	
	<!-- Bootstrap CSS -->
	<title>The Fruit Machine</title>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
</head>
<body>
	<div class="container">
		<h1>The Fruit Machine</h1>
'''

def page_foot():
	return '''
	</div><!-- class="container" -->
	<!-- Optional JavaScript -->
	<!-- jQuery first, then Popper.js, then Bootstrap JS -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

</body>
</html>
'''


