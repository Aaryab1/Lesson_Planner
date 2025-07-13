import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Paper,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
  Link,
} from '@mui/material';
import {
  School,
  Schedule,
  Flag,
  Build,
  Book,
  Assignment,
  Quiz,
  Link as LinkIcon,
  ExpandMore,
  AccessTime,
  CheckCircle,
  Science,
  Group,
} from '@mui/icons-material';
import { LessonPlan } from '../types/lessonPlan';

interface LessonPlanDisplayProps {
  lessonPlan: LessonPlan;
  onBack: () => void;
}

export const LessonPlanDisplay: React.FC<LessonPlanDisplayProps> = ({ lessonPlan, onBack }) => {
  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins} minutes`;
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      <Button
        variant="outlined"
        onClick={onBack}
        startIcon={<School />}
        sx={{ mb: 3 }}
      >
        Create New Lesson Plan
      </Button>

      <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <School sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography variant="h3" component="h1" gutterBottom>
            {lessonPlan.topic}
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mb: 2 }}>
            <Chip
              icon={<School />}
              label={lessonPlan.grade_level}
              color="primary"
              variant="outlined"
            />
            <Chip
              icon={<Schedule />}
              label={formatDuration(lessonPlan.duration_minutes)}
              color="secondary"
              variant="outlined"
            />
          </Box>
        </Box>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {/* Top Row - Learning Objectives and Materials */}
          <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            {/* Learning Objectives */}
            <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
              <Card elevation={2}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Flag color="primary" />
                    Learning Objectives
                  </Typography>
                  <List dense>
                    {lessonPlan.learning_objectives.map((objective, index) => (
                      <ListItem key={index} sx={{ pl: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <CheckCircle color="primary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={objective} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Box>

            {/* Materials Needed */}
            <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
              <Card elevation={2}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Build color="primary" />
                    Materials Needed
                  </Typography>
                  <List dense>
                    {lessonPlan.materials_needed.map((material, index) => (
                      <ListItem key={index} sx={{ pl: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <Science color="secondary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={material} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Box>
          </Box>

          {/* Lesson Overview */}
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Book color="primary" />
                Lesson Overview
              </Typography>
              <Box sx={{ mt: 2 }}>
                {lessonPlan.lesson_overview.map((topic, index) => (
                  <Accordion key={index} sx={{ mb: 1 }}>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                        <Typography variant="subtitle1" sx={{ flexGrow: 1 }}>
                          {topic.title}
                        </Typography>
                        <Chip
                          icon={<AccessTime />}
                          label={formatDuration(topic.duration_minutes)}
                          size="small"
                          color="secondary"
                          variant="outlined"
                        />
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2" color="text.secondary">
                        {topic.description}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                ))}
              </Box>
            </CardContent>
          </Card>

          {/* Bottom Row - Exercises and Assessment */}
          <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            {/* Exercises */}
            <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
              <Card elevation={2}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Assignment color="primary" />
                    Classroom Exercises
                  </Typography>
                  <List dense>
                    {lessonPlan.exercises.map((exercise, index) => (
                      <ListItem key={index} sx={{ pl: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <Group color="primary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={exercise} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Box>

            {/* Assessment */}
            <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
              <Card elevation={2}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Quiz color="primary" />
                    Assessment Questions
                  </Typography>
                  <List dense>
                    {lessonPlan.assessment.map((question, index) => (
                      <ListItem key={index} sx={{ pl: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <CheckCircle color="secondary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={question} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Box>
          </Box>

          {/* Source URLs */}
          {lessonPlan.urls.length > 0 && (
            <Card elevation={2}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <LinkIcon color="primary" />
                  Source Materials
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {lessonPlan.urls.map((url, index) => (
                    <Link
                      key={index}
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      sx={{ textDecoration: 'none' }}
                    >
                      <Chip
                        label={`Source ${index + 1}`}
                        variant="outlined"
                        clickable
                        icon={<LinkIcon />}
                      />
                    </Link>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}
        </Box>
      </Paper>
    </Box>
  );
}; 