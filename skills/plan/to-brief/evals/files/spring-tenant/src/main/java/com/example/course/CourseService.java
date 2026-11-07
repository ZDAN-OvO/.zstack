package com.example.course;

import java.util.List;

public class CourseService {
    private final CourseMapper mapper;
    public CourseService(CourseMapper mapper) { this.mapper = mapper; }
    // 只按 createBy 过滤，没有 tenant_id 条件
    public List<Course> pageTeachingCourses(long userId) { return mapper.selectByCreator(userId); }
}
