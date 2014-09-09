import simuvex
from simuvex.s_type import SimTypeString, SimTypeInt

######################################
# puts
######################################

class puts(simuvex.SimProcedure):
	def __init__(self): # pylint: disable=W0231,
		self.argument_types = {0: self.ty_ptr(SimTypeString())}
		self.return_type = SimTypeInt(32, True)

		write = simuvex.SimProcedures['syscalls']['write']
		strlen = simuvex.SimProcedures['libc.so.6']['strlen']

		string = self.arg(0)
		length = self.inline_call(strlen, string).ret_expr

		self.inline_call(write, self.state.BVV(1, self.state.arch.bits), string, length)
		plugin = self.state['posix']
		self.add_refs(simuvex.SimFileWrite(self.addr, self.stmt_from, 1, plugin.pos(1), self.state.BVV(0x0a, 8), 1))
		plugin.write(1, self.state.BVV(0x0a, 8), 1)

		# TODO: return values
		self.ret()
