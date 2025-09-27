import React, { useState } from 'react';
import { Container, Row, Col, Form, Image, Tabs, Tab } from 'react-bootstrap';
import { Card, Button, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Pic1 from './assets/pic1.png'
import Pic2 from './assets/pic2.png'
import Pic3 from './assets/pic3.png'
import Pic4 from './assets/pic4.png'
import Pic5 from './assets/pic5.png'
import Pic6 from './assets/pic6.png'

const mockSources = [
  {
    location: 'Rajm Khashman – Muslan, Al Ahmadi, Kuwait',
    data: [
      ['Source Emission Rate', '12.5 kg CH4/hr'],
      ['Source Persistence', '87%'],
      ['Number of Plumes', '5'],
      ['Days Observed', '14'],
    ],
  },
  {
    location: 'Al Safa – Riyadh, Saudi Arabia',
    data: [
      ['Source Emission Rate', '8.2 kg CH4/hr'],
      ['Source Persistence', '65%'],
      ['Number of Plumes', '3'],
      ['Days Observed', '9'],
    ],
  },
  {
    location: 'Jebel Ali – Dubai, UAE',
    data: [
      ['Source Emission Rate', '15.1 kg CH4/hr'],
      ['Source Persistence', '92%'],
      ['Number of Plumes', '7'],
      ['Days Observed', '18'],
    ],
  }, {
    location: 'Jebel Ali – Dubai, UAE',
    data: [
      ['Source Emission Rate', '15.1 kg CH4/hr'],
      ['Source Persistence', '92%'],
      ['Number of Plumes', '7'],
      ['Days Observed', '18'],
    ],
  },
  {
    location: 'Jebel Ali – Dubai, UAE',
    data: [
      ['Source Emission Rate', '15.1 kg CH4/hr'],
      ['Source Persistence', '92%'],
      ['Number of Plumes', '7'],
      ['Days Observed', '18'],
    ],
  },
  {
    location: 'Basra Industrial – Basra, Iraq',
    data: [
      ['Source Emission Rate', '6.7 kg CH4/hr'],
      ['Source Persistence', '48%'],
      ['Number of Plumes', '2'],
      ['Days Observed', '6'],
    ],
  },
];


function App() {
  const images = [
    Pic1,
    Pic2,
    Pic3,
    Pic4,
    Pic5,
    Pic6
  ];

  const [searchText, setSearchText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const currentSource = mockSources[currentIndex];

  const handleClick = (e) => {
    if (e.target.tagName.toLowerCase() === 'input') return;
    // if (currentIndex !== images.length - 1) {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    // }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  }

  return (
    <Container fluid className="vh-100 vw-100 overflow-hidden">
      <Row className="h-100">
        <Col
          md={10}
          className="bg-dark text-white position-relative d-flex align-items-center justify-content-center"
          onClick={handleClick}
          style={{
            cursor: 'pointer',
            backgroundImage: `url(${images[currentIndex]})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            transition: "background-image 1s ease-in-out"
          }}
        >
          <div
            className="position-absolute top-0 start-0 w-100 p-3"
            style={{ zIndex: 10 }}
          >
            <Form onSubmit={handleSubmit}>
              <Form.Control
                type="text"
                placeholder="Search by coordinates or facility name"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                className="rounded-pill shadow-sm"
              />
            </Form>
          </div>
        </Col>


        <Col
          md={2}
          className="bg-light p-4 shadow-sm rounded d-flex flex-column align-items-start"
          style={{
            fontFamily: 'Inter, sans-serif',
            overflowY: 'auto',
            maxHeight: '100%',
            borderLeft: '1px solid #eee',
          }}
        >
          <div className="mb-3 w-100">
            <h6 className="fw-semibold text-muted mb-1">Facility Location</h6>
            <h5 className="fw-bold text-dark">{currentSource.location}</h5>
          </div>

          <Tabs defaultActiveKey="plumes" id="plumes-support-tabs" className="custom-tabs w-100 mb-3">
            <Tab eventKey="plumes" title="Plumes">
              <div className="mt-3">
                {currentSource.data.map(([label, value]) => (
                  <div className="d-flex justify-content-between align-items-center mb-2" key={label}>
                    <span className="text-muted">{label}</span>
                    <span
                      className="px-3 py-1 rounded-pill fw-semibold ms-4"
                      style={{
                        backgroundColor: '#f0f0f0',
                        color: '#333',
                        fontSize: '0.9rem',
                        minWidth: '80px',
                        textAlign: 'center',
                      }}
                    >
                      {value}
                    </span>
                  </div>
                ))}
              </div>

            </Tab>
            <Tab eventKey="supporting" title="More Details">
            </Tab>
          </Tabs>
          <Card
            className="w-100 mb-3 mt-3"
            style={{
              border: '2px solid #8B0000',
              backgroundColor: '#f8f9fa',
              borderRadius: '0px',
            }}
          >
            <Card.Body>
              <Card.Title style={{ color: '#8B0000', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                Warning
              </Card.Title>
              <Card.Text style={{ color: '#8B0000' }}>
                The emission is high and may require immediate attention.
              </Card.Text>
            </Card.Body>
          </Card>

        </Col>

      </Row>
    </Container>
  );
}


export default App;
