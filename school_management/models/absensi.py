from odoo import fields, models, api, _
from datetime import date, datetime
from odoo.exceptions import UserError

class SchoolAbsensi(models.Model):
    _name = 'school.absensi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Pertemuan")
    day = fields.Date(string="Tanggal", required=True, default=date.today())
    date_start = fields.Datetime(string="Jam Mulai")
    date_end = fields.Datetime(string="Jam Selesai")
    state = fields.Selection([('undone', 'Belum Dimulai'), ('ongoing', 'Sedang Berlangsung'), ('done', 'Selesai')],
                             'Status',
                             default='undone', tracking=True)
    pelajaran_id = fields.Many2one(string='Pelajaran', comodel_name='school.pelajaran', required=True, tracking=True)
    kelas_id = fields.Many2one(string='Kelas', comodel_name='school.kelas', required=True)
    guru_id = fields.Many2one(string='Guru', comodel_name='res.users', domain=[('is_guru', '=', True)], required=True,
                              default=lambda self: self.env.user)

    murid_ids = fields.Many2many('res.partner', domain="[('kelas_id', '=', kelas_id), ('is_murid', '=', True)]",
                                 string="Murid")
    
    @api.constrains('pelajaran_id', 'day', 'kelas_id')
    def check_pelajaran_day(self):
        existing_record = self.search([
                ('day', '=', self.day),
                ('pelajaran_id', '=', self.pelajaran_id.id),
                ('kelas_id', '=', self.kelas_id.id),
                ('id', '!=', self.id)
            ])
        if existing_record:
            raise UserError('Tidak boleh membuat absensi dengan pelajaran dan kelas yang sama pada tanggal yang sama')

    # Check apabila ada pertemuan dan pelajaran yang sama
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('school.absensi')
        return super(SchoolAbsensi, self).create(vals)

    # Tampilkan Murid yang ada di kelas yang dipilih
    @api.onchange('kelas_id')
    def _onchange_kelas_id(self):
        for rec in self:
            return {'domain': {'murid_ids': [('id', 'in', rec.kelas_id.murid_ids.ids)]}}

    # Tampilkan Guru yang ada di pelajaran yang dipilih
    @api.onchange('pelajaran_id')
    def _onchange_pelajaran_id(self):
        for rec in self:
            return {'domain': {'guru_id': [('id', 'in', rec.pelajaran_id.guru_ids.ids)]}}

    def action_mulai_kelas(self):
        self.state = 'ongoing'
        self.date_start = datetime.now()

    def action_akhiri_kelas(self):
        self.state = 'done'
        self.date_end = datetime.now()
