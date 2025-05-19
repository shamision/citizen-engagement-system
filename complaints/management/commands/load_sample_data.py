# complaints/management/commands/load_sample_data.py

from django.core.management.base import BaseCommand
from complaints.models import Agency, Category, Complaint, Response
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Load sample data for the Citizen Engagement System'

    def handle(self, *args, **kwargs):
        # Create agencies
        self.stdout.write('Creating agencies...')
        agencies = [
            Agency.objects.create(
                name='Roads and Transport Department',
                description='Handles road infrastructure and public transport issues',
                email='roads@government.rw',
                phone='(250) 78-123-4567'
            ),
            Agency.objects.create(
                name='Water and Sanitation Department',
                description='Handles water supply and sanitation issues',
                email='water@government.rw',
                phone='(250) 78-234-5678'
            ),
            Agency.objects.create(
                name='Electricity Department',
                description='Handles electricity supply and infrastructure issues',
                email='electricity@government.rw',
                phone='(250) 78-345-6789'
            ),
            Agency.objects.create(
                name='Health Services Department',
                description='Handles public health issues and hospital services',
                email='health@government.rw',
                phone='(250) 78-456-7890'
            ),
        ]
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories = [
            Category.objects.create(name='Road Maintenance', description='Issues related to road conditions', agency=agencies[0]),
            Category.objects.create(name='Public Transport', description='Issues related to public transportation', agency=agencies[0]),
            Category.objects.create(name='Water Supply', description='Issues related to water availability and quality', agency=agencies[1]),
            Category.objects.create(name='Drainage and Sewage', description='Issues related to drainage and sewage systems', agency=agencies[1]),
            Category.objects.create(name='Power Outages', description='Issues related to electricity outages', agency=agencies[2]),
            Category.objects.create(name='Electrical Infrastructure', description='Issues related to electrical poles, cables, etc.', agency=agencies[2]),
            Category.objects.create(name='Public Health', description='Issues related to public health concerns', agency=agencies[3]),
            Category.objects.create(name='Hospital Services', description='Issues related to government hospitals', agency=agencies[3]),
        ]
        
        # Create sample complaints
        self.stdout.write('Creating sample complaints...')
        statuses = ['submitted', 'under_review', 'in_progress', 'resolved', 'closed']
        
        complaint_data = [
            {
                'category': categories[0],
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '(250) 78-111-2222',
                'subject': 'Pothole on Main Street',
                'description': 'There is a large pothole on Main Street near the central market that has been causing accidents.',
                'location': 'Main Street, Central District, Kigali',
            },
            {
                'category': categories[2],
                'name': 'Alice Smith',
                'email': 'alice.smith@example.com',
                'phone': '(250) 78-222-3333',
                'subject': 'No water supply for 3 days',
                'description': 'Our neighborhood has not had water for the past 3 days. We need this resolved urgently.',
                'location': 'Kimironko, Kigali',
            },
            {
                'category': categories[4],
                'name': 'Robert Johnson',
                'email': 'robert.j@example.com',
                'phone': '(250) 78-333-4444',
                'subject': 'Frequent power outages',
                'description': 'We have been experiencing power outages almost daily for the past week, each lasting several hours.',
                'location': 'Nyamirambo, Kigali',
            },
            {
                'category': categories[6],
                'name': 'Mary Williams',
                'email': 'mary.w@example.com',
                'phone': '(250) 78-444-5555',
                'subject': 'Garbage not collected',
                'description': 'The garbage in our area has not been collected for two weeks, causing health concerns.',
                'location': 'Gikondo, Kigali',
            },
        ]
        
        complaints = []
        for data in complaint_data:
            status = random.choice(statuses)
            complaint = Complaint.objects.create(
                category=data['category'],
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                subject=data['subject'],
                description=data['description'],
                location=data['location'],
                status=status,
            )
            complaints.append(complaint)
        
        # Create responses for some complaints
        self.stdout.write('Creating sample responses...')
        for complaint in complaints:
            if complaint.status not in ['submitted']:
                Response.objects.create(
                    complaint=complaint,
                    responder_name='Official Response Team',
                    responder_title='Customer Service Officer',
                    content='Thank you for bringing this to our attention. We have registered your complaint and will investigate the issue.',
                )
            
            if complaint.status in ['in_progress', 'resolved', 'closed']:
                Response.objects.create(
                    complaint=complaint,
                    responder_name='Department Manager',
                    responder_title='Operations Supervisor',
                    content='Our team has been assigned to address this issue. We expect to resolve it within the next 48 hours.',
                )
            
            if complaint.status in ['resolved', 'closed']:
                Response.objects.create(
                    complaint=complaint,
                    responder_name='Resolution Team',
                    responder_title='Field Engineer',
                    content='We are pleased to inform you that the reported issue has been resolved. Please let us know if you have any further concerns.',
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))