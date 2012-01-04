#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

def clients_stats(type, jid, nick, text):
	text = reduce_spaces_all(text).lower().split()
	if text:
		is_short = 'short' in text
		is_global = 'global' in text or 'total' in text or 'all' in text
		if is_short or is_global:
			for t in ['all','total','global','short']:
				if t in text: text.remove(t)
		if text: match = '%%\r%%%s%%' % ' '.join(text)
		else: match = '%\r%' 
	else:
		match = '%\r%'
		is_short = is_global = False
	if is_global: req,par = 'select message from age where message ilike %s',(match,)
	else: req,par = 'select message from age where room=%s and message ilike %s',(jid,match)
	st = cur_execute_fetchall(req,par)
	if st:
		ns = {}
		et = L('Error! %s')%''
		for t in st:
			k = t[0].split('\r',1)[1].split(' // ')[0].replace('\r','[LF]').replace('\n','[CR]').replace('\t','[TAB]')
			if is_short: k = k.split()[0]
			if not k.startswith(et.strip()):
				if ns.has_key(k): ns[k] += 1
				else: ns[k] = 1
		ns = [(ns[t],t) for t in ns.keys()]
		ns.sort(reverse=True)
		msg = L('Client statistic:\n%s') % '\n'.join(['%s. %s\t%s' % (ns.index(t)+1,t[1],t[0]) for t in ns[:10]])
	else: msg = L('Clients statistic not available.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(4, 'clients', clients_stats, 2, L('Show clients statistic when available.\nclients [total|global|all[ short]] [string]'))]
