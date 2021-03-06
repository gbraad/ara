import json

from flask import render_template, abort, Blueprint
from ara import models, utils

host = Blueprint('host', __name__)


@host.route('/')
def host_summary():
    hosts = models.Host.query.order_by(models.Host.name)
    stats = utils.get_summary_stats(hosts, 'host_id')

    return render_template('host_summary.html',
                           hosts=hosts,
                           stats=stats)


@host.route('/<host>/')
def show_host(host):
    try:
        host = models.Host.query.filter_by(name=host).one()
    except models.NoResultFound:
        abort(404)

    stats = utils.get_host_playbook_stats(host)

    return render_template('host.html', host=host, stats=stats)


@host.route('/<host>/facts/')
def show_facts(host):
    try:
        host = models.Host.query.filter_by(name=host).one()
    except models.NoResultFound:
        abort(404)

    if not host.facts:
        abort(404)
    else:
        facts = json.loads(host.facts.values).iteritems()

    return render_template('host_facts.html', host=host, facts=facts)
